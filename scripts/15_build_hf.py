"""Stage the Hugging Face dataset in out/hf/ and check it against the monthly files.

Tables: meetings, attendees, documents (manifest joined to the listing). Files: handouts/<month>/<document_id><ext>
and text/<month>/<document_id>.txt. Every manifest row must have its file, with the recorded size and SHA-256.
"""
import csv, glob, hashlib, os, shutil, sys
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
OUT = "out/hf"
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT + "/data")


def months():
    return sorted(os.path.basename(f)[:7] for f in glob.glob("data/20??-??_meetings.csv"))


def load(kind):
    frames = []
    for m in months():
        df = pd.read_csv(f"data/{m}_{kind}.csv", dtype=str, keep_default_na=False)
        df.insert(0, "month", m)
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


meetings, attendees = load("meetings"), load("attendees")
listed, manifest = load("documents_listed"), load("document_manifest")
assert meetings["meeting_id"].is_unique
assert set(attendees["meeting_id"]) <= set(meetings["meeting_id"])
docs = manifest.merge(listed[["document_id", "title"]], on="document_id", how="left")
assert len(docs) == len(listed), (len(docs), len(listed))
assert docs["document_id"].is_unique

bad = []
paths, tpaths = [], []
for r in docs.itertuples():
    src = f"downloads/{r.month}/{r.document_id}.bin"
    ext = os.path.splitext(r.file_name or "")[1].lower()[:6] or ".bin"
    rel = f"handouts/{r.month}/{r.document_id}{ext}"
    if not os.path.exists(src):
        bad.append((r.document_id, "missing file")); paths.append(""); tpaths.append(""); continue
    h = hashlib.sha256(open(src, "rb").read()).hexdigest()
    if h != r.sha256 or os.path.getsize(src) != int(r.size_bytes):
        bad.append((r.document_id, "hash or size differs from manifest"))
    os.makedirs(f"{OUT}/handouts/{r.month}", exist_ok=True)
    os.link(src, f"{OUT}/{rel}")
    paths.append(rel)
    t = f"downloads/{r.month}_text/{r.document_id}.txt"
    if r.text_extracted == "yes" and os.path.exists(t):
        trel = f"text/{r.month}/{r.document_id}.txt"
        os.makedirs(f"{OUT}/text/{r.month}", exist_ok=True)
        os.link(t, f"{OUT}/{trel}")
        tpaths.append(trel)
    else:
        tpaths.append("")
docs["handout_path"], docs["text_path"] = paths, tpaths
meetings.to_parquet(f"{OUT}/data/meetings.parquet", index=False)
attendees.to_parquet(f"{OUT}/data/attendees.parquet", index=False)
docs.to_parquet(f"{OUT}/data/documents.parquet", index=False)
print("meetings", len(meetings), "attendees", len(attendees), "documents", len(docs),
      "with text", sum(1 for t in tpaths if t), "problems", len(bad))
for b in bad[:20]:
    print(b)
sys.exit(1 if bad else 0)
