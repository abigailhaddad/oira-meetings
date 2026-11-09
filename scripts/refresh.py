"""Weekly refresh: re-read the last two months from reginfo.gov, merge into the Hugging Face dataset, upload.

    python scripts/refresh.py            # needs HF_TOKEN
    python scripts/refresh.py --dry-run  # everything except the upload

Hugging Face is the state. The window is the previous month plus this month through today, because
a meeting can be rescheduled or get handouts after it is first listed. New data wins by meeting_id and
document_id; rows outside the window, and rows the site no longer lists, are kept. The run stops without
uploading if a month fails, if the site returns nothing for a window that had meetings, or if it would
shrink the dataset.
"""
import calendar, csv, datetime, glob, hashlib, json, os, subprocess, sys
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
REPO = "abigailhaddad/oira-eo12866-meetings"
B = f"https://huggingface.co/datasets/{REPO}/resolve/main/data/"


def window(today):
    first = today.replace(day=1)
    prev = (first - datetime.timedelta(days=1))
    out = []
    for y, m, end in ((prev.year, prev.month, prev.replace(day=calendar.monthrange(prev.year, prev.month)[1])),
                      (today.year, today.month, today)):
        out.append((f"{y}-{m:02d}", f"{m:02d}/01/{y}", end.strftime("%m/%d/%Y")))
    return out


def merge_by_key(old, new, key):
    """New rows win by key; rows only in old are kept."""
    kept = old[~old[key].isin(set(new[key]))]
    return pd.concat([new, kept], ignore_index=True)


def merge_attendees(old, new, new_meeting_ids):
    """Attendees have no key of their own: replace every row of each meeting the new run covered."""
    kept = old[~old["meeting_id"].isin(set(new_meeting_ids))]
    return pd.concat([new, kept], ignore_index=True)


def run(args):
    r = subprocess.run([sys.executable] + args, cwd=SCRIPTS)
    if r.returncode != 0:
        sys.exit(f"step failed: {args[:2]} (exit {r.returncode}); nothing uploaded")


def load_month(tag, kind):
    df = pd.read_csv(os.path.join(ROOT, "data", f"{tag}_{kind}.csv"), dtype=str, keep_default_na=False)
    df.insert(0, "month", tag)
    return df


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main():
    dry = "--dry-run" in sys.argv
    only = sys.argv[sys.argv.index("--months") + 1].split(",") if "--months" in sys.argv else None
    today = datetime.date.today()
    old_m = pd.read_parquet(B + "meetings.parquet")
    old_a = pd.read_parquet(B + "attendees.parquet")
    old_d = pd.read_parquet(B + "documents.parquet")

    new_m, new_a, new_d = [], [], []
    for tag, start, end in window(today):
        if only and tag not in only:
            continue
        for f in glob.glob(os.path.join(ROOT, "data", f"{tag}_*")):
            os.remove(f)  # never merge a stale file from an earlier run
        run(["01_list_month.py", start, end, tag, "nopage"])
        banner = json.load(open(os.path.join(ROOT, "data", f"{tag}_search.json")))["found_banner"]
        had = int((old_m["month"] == tag).sum())
        if banner == 0 and had > 0:
            sys.exit(f"{tag}: site says 0 meetings but we hold {had}; nothing uploaded")
        if banner == 0:
            continue
        run(["02_fetch_meetings.py", tag])
        mj = json.load(open(os.path.join(ROOT, "data", f"{tag}_meetings.json")))
        if mj["fetch_failures"]:
            sys.exit(f"{tag}: meeting page failures {mj['fetch_failures'][:5]}; nothing uploaded")
        run(["13_add_requestor_client.py"])  # re-reads the saved HTML; adds requestor_client to this month's CSV
        run(["03_download_docs.py", tag])
        run(["-I", "05_extract_text.py", tag])
        m = load_month(tag, "meetings")
        if len(m) != banner:
            sys.exit(f"{tag}: {len(m)} meetings collected but the site banner says {banner}; nothing uploaded")
        new_m.append(m)
        new_a.append(load_month(tag, "attendees"))
        listed, man = load_month(tag, "documents_listed"), load_month(tag, "document_manifest")
        new_d.append(man.merge(listed[["document_id", "title"]], on="document_id", how="left"))

    if not new_m:
        print("nothing new in the window")
        return
    nm, na, nd = (pd.concat(x, ignore_index=True) for x in (new_m, new_a, new_d))
    ops = []  # (path in repo, local path)
    hp, tp = [], []
    old_sha = dict(zip(old_d["document_id"], old_d["sha256"]))
    for r in nd.itertuples():
        src = os.path.join(ROOT, "downloads", r.month, f"{r.document_id}.bin")
        ext = os.path.splitext(r.file_name or "")[1].lower()[:6] or ".bin"
        rel = f"handouts/{r.month}/{r.document_id}{ext}"
        if not os.path.exists(src):
            sys.exit(f"document {r.document_id}: no downloaded file; nothing uploaded")
        if sha(src) != r.sha256:
            sys.exit(f"document {r.document_id}: hash differs from manifest; nothing uploaded")
        hp.append(rel)
        t = os.path.join(ROOT, "downloads", f"{r.month}_text", f"{r.document_id}.txt")
        trel = f"text/{r.month}/{r.document_id}.txt" if r.text_extracted == "yes" and os.path.exists(t) else ""
        tp.append(trel)
        if old_sha.get(r.document_id) != r.sha256:
            ops.append((rel, src))
            if trel:
                ops.append((trel, t))
    nd["handout_path"], nd["text_path"] = hp, tp

    meetings = merge_by_key(old_m, nm, "meeting_id")
    attendees = merge_attendees(old_a, na, nm["meeting_id"])
    docs = merge_by_key(old_d, nd, "document_id")
    if len(meetings) < len(old_m) or len(docs) < len(old_d):
        sys.exit("would shrink the dataset; nothing uploaded")
    assert meetings["meeting_id"].is_unique and docs["document_id"].is_unique
    added_m = len(set(nm["meeting_id"]) - set(old_m["meeting_id"]))
    common = [c for c in nm.columns if c in old_m.columns and c not in ("month", "meeting_id")]
    ex = nm[nm["meeting_id"].isin(set(old_m["meeting_id"]))].set_index("meeting_id")[common]
    was = old_m.set_index("meeting_id").loc[ex.index, common]
    changed_m = int((ex.astype(str) != was.astype(str)).any(axis=1).sum())
    assert list(nm.columns) == list(old_m.columns), (list(nm.columns), list(old_m.columns))
    summary = dict(as_of=today.isoformat(), meetings=len(meetings), added_meetings=added_m,
                   changed_meetings=changed_m, documents=len(docs), new_files=len(ops))
    print(summary)
    os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
    for name, df in (("meetings", meetings), ("attendees", attendees), ("documents", docs)):
        df.to_parquet(os.path.join(ROOT, "out", f"{name}.parquet"), index=False)
    if dry:
        print("dry run: nothing uploaded")
        return
    if added_m == 0 and changed_m == 0 and not ops:
        print("no change; nothing uploaded")
        return
    from huggingface_hub import CommitOperationAdd, HfApi
    adds = [CommitOperationAdd(path_in_repo=f"data/{n}.parquet", path_or_fileobj=os.path.join(ROOT, "out", f"{n}.parquet"))
            for n in ("meetings", "attendees", "documents")]
    adds += [CommitOperationAdd(path_in_repo=rel, path_or_fileobj=src) for rel, src in ops]
    HfApi().create_commit(repo_id=REPO, repo_type="dataset", operations=adds,
                          commit_message=f"Refresh {today}: +{added_m} meetings, {changed_m} changed, {len(ops)} files")


if __name__ == "__main__":
    main()
