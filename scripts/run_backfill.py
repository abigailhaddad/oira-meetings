"""Backfill driver: month by month, newest first, from 2026-11 back to 2025-01 (starting 2025-01-20).
Resume: just re-run; months with data/<tag>_DONE.json are skipped. Stops (cleanly, at a month boundary) on: block (403/429), request budget,
low disk, handouts over the size cap, or after the start-new-month deadline.
Usage: python run_backfill.py [--deadline HH:MM] (local time)"""
import sys, os, re, json, csv, shutil, subprocess, calendar, datetime
from bs4 import BeautifulSoup
from common import *
DEADLINE = sys.argv[sys.argv.index("--deadline") + 1] if "--deadline" in sys.argv else "20:05"
MAX_REQ, MIN_FREE_GB, MAX_DL_BYTES = 4300, 4.5, 2.4e9
D = os.path.dirname(os.path.abspath(__file__)); PY = sys.executable
def nreq(): return sum(1 for _ in open(LOG))
def free_gb(): return shutil.disk_usage(D).free / 1e9
def dl_bytes():
    t = 0
    for r, _, fs in os.walk(f"{D}/../downloads"):
        t += sum(os.path.getsize(os.path.join(r, f)) for f in fs)
    return t
def months():
    out = []; y, m = 2026, 11
    while (y, m) >= (2025, 1):
        last = calendar.monthrange(y, m)[1]
        start = "01/20/2025" if (y, m) == (2025, 1) else f"{m:02d}/01/{y}"
        end = f"{m:02d}/{min(last, 8) if (y, m) == (2026, 11) else last:02d}/{y}"
        out.append((f"{y}-{m:02d}", start, end)); m -= 1
        if m == 0: y, m = y - 1, 12
    return out
def parse(h):
    s = BeautifulSoup(h, "lxml"); mm = re.search(r"Number Of Records Found:\s*(\d+)", s.get_text(" ", strip=True))
    ids = [re.search(r"meetingId=(\d+)", a["href"]).group(1) for a in s.find_all("a", href=re.compile(r"viewEO12866Meeting\?"))]
    return (int(mm.group(1)) if mm else 0), ids
def split_check(tag, start, end):
    s = datetime.datetime.strptime(start, "%m/%d/%Y").date(); e = datetime.datetime.strptime(end, "%m/%d/%Y").date()
    ids, banners, nreqs = set(), 0, 0; cur = s
    while cur <= e:
        nxt = min(cur + datetime.timedelta(days=6), e)
        r = get(BASE + "/public/do/eom12866SearchResults", params={"searchStartDate": cur.strftime("%m/%d/%Y"), "searchEndDate": nxt.strftime("%m/%d/%Y"), "operation": "", "resultCount": "1"})
        f, i = parse(r.text)
        if f > len(i):
            r = get(BASE + "/public/do/eom12866SearchResults", params={"viewall": "y", "view": "yes", "viewAllFlag": "Y"}); f2, i = parse(r.text)
        banners += f; ids.update(i); cur = nxt + datetime.timedelta(days=1)
        if f != len(i): print("  split-range banner/rows disagree", f, len(i), flush=True)
    return banners, ids
def run(args):
    r = subprocess.run([PY] + args, cwd=D)
    return r.returncode
def stop(reason):
    print("STOP:", reason, flush=True); sys.exit(0 if reason.startswith("deadline") else 3)
for tag, start, end in months():
    done_fn = f"{D}/../data/{tag}_DONE.json"
    reverify = tag == "2026-10" and os.path.exists(done_fn) and not os.path.exists(f"{D}/../data/2026-10_reverify.json")
    if os.path.exists(done_fn) and not reverify: continue
    now = datetime.datetime.now().strftime("%H:%M")
    if now >= DEADLINE: stop(f"deadline {DEADLINE} reached before {tag}")
    if nreq() > MAX_REQ: stop(f"request budget ({nreq()})")
    if free_gb() < MIN_FREE_GB: stop(f"free disk {free_gb():.1f} GB")
    if dl_bytes() > MAX_DL_BYTES: stop(f"downloads {dl_bytes()/1e9:.2f} GB")
    print(f"=== {tag} {start}-{end} (requests so far {nreq()}, free {free_gb():.1f} GB, downloads {dl_bytes()/1e9:.2f} GB)", flush=True)
    t0 = nreq()
    if reverify:
        banners, ids = split_check(tag, start, end)
        r = get(BASE + "/public/do/eom12866SearchResults", params={"searchStartDate": start, "searchEndDate": end, "operation": "", "resultCount": "1"})
        banner_now, _ = parse(r.text)
        mine = {m["meeting_id"] for m in csv.DictReader(open(f"{D}/../data/2026-10_meetings.csv"))}
        json.dump(dict(checked_at=time.strftime("%Y-%m-%d %H:%M:%S %Z"), banner_now=banner_now, split_banner_sum=banners, split_union=len(ids), stored_ids=len(mine), union_eq_stored=ids == mine,
                       only_live=sorted(ids - mine), only_stored=sorted(mine - ids)), open(f"{D}/../data/2026-10_reverify.json", "w"), indent=1)
        print("reverify Oct:", banner_now, banners, len(ids), ids == mine, flush=True); continue
    for step in (["01_list_month.py", start, end, tag, "nopage"], ["02_fetch_meetings.py", tag]):
        if run(step) != 0: stop(f"step failed/blocked: {step[0]} for {tag}")
    srch = json.load(open(f"{D}/../data/{tag}_search.json")); banner = srch["found_banner"]
    uniq = {x["meeting_id"] for x in srch["rows_viewall"]}
    mj = json.load(open(f"{D}/../data/{tag}_meetings.json"))
    if mj["fetch_failures"]: stop(f"meeting page failures in {tag}: {mj['fetch_failures'][:5]} (re-run resumes)")
    if free_gb() < MIN_FREE_GB: stop(f"free disk {free_gb():.1f} GB")
    if run(["03_download_docs.py", tag]) != 0: stop(f"download step failed/blocked for {tag}")
    if run(["-I", "05_extract_text.py", tag]) != 0: stop(f"extract step failed for {tag}")
    banners, ids = split_check(tag, start, end)
    dl = json.load(open(f"{D}/../data/{tag}_downloads.json")) if os.path.exists(f"{D}/../data/{tag}_downloads.json") else {}
    man = list(csv.DictReader(open(f"{D}/../data/{tag}_document_manifest.csv")))
    stats = dict(tag=tag, start=start, end=end, banner=banner, viewall_rows=len(srch["rows_viewall"]), unique_ids=len(uniq), meetings_fetched=len(mj["meetings"]),
                 split_banner_sum=banners, split_union=len(ids), split_union_eq_month=ids == uniq, docs_listed=len(mj["documents"]),
                 docs_downloaded_ok=sum(1 for v in dl.values() if v.get("status") == 200), docs_failed=[k for k, v in dl.items() if v.get("status") != 200],
                 docs_no_text=[r["document_id"] for r in man if r["text_extracted"] != "yes"], bytes=sum(int(r["size_bytes"] or 0) for r in man),
                 requests_this_month=nreq() - t0, finished=time.strftime("%Y-%m-%d %H:%M:%S %Z"))
    json.dump(stats, open(done_fn, "w"), indent=1)
    print({k: v for k, v in stats.items() if k not in ("docs_no_text",)}, flush=True)
    if banner != len(uniq) or not stats["split_union_eq_month"]: print("  !! DISAGREEMENT in", tag, flush=True)
print("ALL MONTHS DONE", flush=True)
