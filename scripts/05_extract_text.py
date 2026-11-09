"""Step 5: per-document manifest (sizes, hashes, pages, text extraction). Run with: python -I 05_extract_text.py 2026-10
Files are untrusted: only pdfinfo/pdftotext (poppler, with timeouts) and zipfile XML text-scraping are used; nothing is opened by an office app."""
import sys, os, csv, json, re, subprocess, zipfile, hashlib
TAG = sys.argv[1]
D = os.path.dirname(os.path.abspath(__file__))
DL = f"{D}/../downloads/{TAG}"; TX = f"{D}/../downloads/{TAG}_text"; os.makedirs(TX, exist_ok=True)
dl = json.load(open(f"{D}/../data/{TAG}_downloads.json"))
listed = list(csv.DictReader(open(f"{D}/../data/{TAG}_documents_listed.csv")))
meet = {m["meeting_id"]: m for m in csv.DictReader(open(f"{D}/../data/{TAG}_meetings.csv"))}
def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=120, errors="replace")
def ooxml_text(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        parts = [n for n in names if re.match(r"(word/document|ppt/slides/slide\d+|xl/sharedStrings)\.xml$", n)]
        out = []
        for n in sorted(parts):
            if z.getinfo(n).file_size > 50_000_000: continue
            x = z.read(n).decode("utf8", "replace")
            out.append(" ".join(re.findall(r"<(?:w:t|a:t|t)(?: [^>]*)?>([^<]*)</", x)))
        n_slides = len([n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)])
    return "\n".join(out), (n_slides or None)
rows = []
for d in listed:
    did = d["document_id"]; info = dl.get(did, {}); path = f"{DL}/{did}.bin"
    if info.get("status") != 200:
        rows.append(dict(meeting_id=d["meeting_id"], document_id=did, listed_title=d["title"], file_name="", file_name_source="", content_type="", file_cmd="", size_bytes="", sha256="", sha256_matches_download_log="", pages_or_slides="", text_chars=0, text_extracted="no", note=f"DOWNLOAD FAILED: {info.get('status')}")); continue
    kind = subprocess.run(["file", "-b", path], capture_output=True, text=True).stdout.strip()
    sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
    rec = dict(meeting_id=d["meeting_id"], document_id=did, listed_title=d["title"], file_name=info["filename"] or "", file_name_source="Content-Disposition" if info["filename"] else "missing (no Content-Disposition; see listed_title)",
               content_type=info["content_type"], file_cmd=kind, size_bytes=info["size"], sha256=sha, sha256_matches_download_log=(sha == info["sha256"]),
               pages_or_slides="", text_chars=0, text_extracted="no", note="")
    txt = ""
    try:
        if "PDF" in kind:
            pi = run(["pdfinfo", path]); m = re.search(r"Pages:\s+(\d+)", pi.stdout)
            rec["pages_or_slides"] = m.group(1) if m else ""
            if pi.returncode != 0: rec["note"] = "pdfinfo error: " + pi.stderr.strip()[:120]
            p = run(["pdftotext", "-layout", path, "-"]); txt = p.stdout
            if p.returncode != 0: rec["note"] += " pdftotext error: " + p.stderr.strip()[:120]
        elif zipfile.is_zipfile(path):
            txt, ns = ooxml_text(path); rec["pages_or_slides"] = ns or ""
            rec["note"] = "OOXML text scraped from XML; pages not counted" if not ns else "slides counted"
        else: rec["note"] = "unrecognised type"
    except Exception as e:
        rec["note"] += f" error: {type(e).__name__}: {e}"[:200]
    body = re.sub(r"\s+", "", txt)
    rec["text_chars"] = len(body)
    pages = int(rec["pages_or_slides"]) if str(rec["pages_or_slides"]).isdigit() else None
    if len(body) >= 50 and (not pages or len(body) / pages >= 100):
        rec["text_extracted"] = "yes"; open(f"{TX}/{did}.txt", "w").write(txt)
    elif len(body) > 0:
        rec["text_extracted"] = "partial/low"; open(f"{TX}/{did}.txt", "w").write(txt); rec["note"] += " low text density (possibly scanned or image-heavy)"
    else:
        rec["note"] += " no text layer (likely scanned/image-only); no OCR performed"
    rows.append(rec)
with open(f"{D}/../data/{TAG}_document_manifest.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["meeting_id","document_id","listed_title","file_name","file_name_source","content_type","file_cmd","size_bytes","sha256","sha256_matches_download_log","pages_or_slides","text_chars","text_extracted","note"]); w.writeheader(); w.writerows(rows)
import collections
print(len(rows), "docs;", collections.Counter(r["text_extracted"] for r in rows), "hash mismatches:", sum(not r["sha256_matches_download_log"] for r in rows), "unique sha:", len({r['sha256'] for r in rows}))
