"""Step 8: spot-check a random sample (+ deliberate edge cases) against the live pages, with a separately written regex parser, a second download
(SHA-256 compare), and a second PDF tool (pypdf) for page counts / text presence. Writes data/<TAG>_proof_sample.{csv,md}."""
import logging; logging.disable(logging.CRITICAL)
import sys, csv, json, os, re, random, hashlib, subprocess, html
from common import *
from pypdf import PdfReader
TAG = sys.argv[1]
meet = {m["meeting_id"]: m for m in csv.DictReader(open(f"../data/{TAG}_meetings.csv"))}
docs = list(csv.DictReader(open(f"../data/{TAG}_documents_listed.csv")))
man = {d["document_id"]: d for d in csv.DictReader(open(f"../data/{TAG}_document_manifest.csv"))}
att = [a for a in csv.DictReader(open(f"../data/{TAG}_attendees.csv"))]
bymeet = {}
for d in docs: bymeet.setdefault(d["meeting_id"], []).append(d)
random.seed(20261108)
with_docs = sorted(bymeet); without = sorted(set(meet) - set(bymeet))
sample = {m: "random (with documents)" for m in random.sample(with_docs, 8)}
for m in random.sample(without, 3): sample.setdefault(m, "random (no documents)")
def edge(label, pred):
    c = [m for m in sorted(meet) if pred(m) and m not in sample]
    if c: sample[c[0]] = label
edge("edge: scanned/no-text PDF", lambda m: any(man[d["document_id"]]["text_extracted"] == "no" for d in bymeet.get(m, [])))
edge("edge: PDF without filename header", lambda m: any(not man[d["document_id"]]["file_name"] for d in bymeet.get(m, [])))
edge("edge: pptx", lambda m: any(man[d["document_id"]]["file_name"].endswith(".pptx") for d in bymeet.get(m, [])))
edge("edge: docx", lambda m: any(man[d["document_id"]]["file_name"].endswith(".docx") for d in bymeet.get(m, [])))
edge("edge: xlsx", lambda m: any(man[d["document_id"]]["file_name"].endswith(".xlsx") for d in bymeet.get(m, [])))
edge("edge: most documents", lambda m: len(bymeet.get(m, [])) == max(len(v) for v in bymeet.values()))
edge("edge: status Scheduled", lambda m: meet[m]["meeting_type"] == "Scheduled")
edge("edge: status No Show", lambda m: meet[m]["meeting_type"] == "No Show")
edge("edge: last meeting of month by date", lambda m: m == sorted(meet, key=lambda k: (meet[k]["meeting_datetime"][6:10], meet[k]["meeting_datetime"][0:5], meet[k]["meeting_datetime"][11:]))[-1])
def txt(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s)).replace("\xa0", " ")).strip()
rows = []; doc_rows = []
for mid, why in sample.items():
    m = meet[mid]
    r = get(BASE + "/public/do/viewEO12866Meeting", params={"viewRule": "false", "rin": m["rin"], "meetingId": mid, "acronym": m["agency"]})
    h = r.text
    live_dt = txt(re.search(r"for=meetingDate>.*?</label>(.*?)</p>", h, re.S).group(1)) if "for=meetingDate" in h else ""
    live_rq = txt(re.search(r"for=requestor>.*?</label>(.*?)<label", h, re.S).group(1)) if "for=requestor>" in h else ""
    live_title = txt(re.search(r"for=\"ruleTitle\">.*?</label>(.*?)</p>", h, re.S).group(1))
    live_docs = re.findall(r"documentID=(\d+)\"\)'>\s*(.*?)\s*</button>", h, re.S)
    live_docs = [(i, txt(t)) for i, t in live_docs]
    live_att = len(re.findall(r'<td align="right" valign="bottom" style="width: 25px">', h))
    ours_docs = [(d["document_id"], re.sub(r"\s+", " ", d["title"]).strip()) for d in bymeet.get(mid, [])]  # whitespace-collapsed on both sides (HTML collapses it)
    rows.append(dict(meeting_id=mid, why=why, link=f"{BASE}/public/do/viewEO12866Meeting?viewRule=false&rin={m['rin']}&meetingId={mid}",
        date_ours=m["meeting_datetime"], date_live=live_dt, date_match=m["meeting_datetime"] == live_dt,
        requestor_ours=m["requestor"], requestor_live=live_rq, requestor_match=m["requestor"] == live_rq, title_match=live_title == m["rule_title"],
        docs_ours=len(ours_docs), docs_live=len(live_docs), docs_match=ours_docs == live_docs,
        attendees_ours=int(m["n_attendees"]), attendees_live=live_att, attendees_match=int(m["n_attendees"]) == live_att))
    for d in bymeet.get(mid, []):
        did = d["document_id"]
        rr = get(BASE + "/public/do/eoDownloadDocument", params={"pubId": "", "eodoc": "true", "documentID": did})
        sha2 = hashlib.sha256(rr.content).hexdigest()
        p = f"../downloads/{TAG}/{did}.bin"; mm = man[did]
        pages2 = ""; text2 = ""
        if mm["content_type"] == "application/pdf":
            try:
                rd = PdfReader(p); pages2 = len(rd.pages); text2 = "yes" if sum(len((pg.extract_text() or "").strip()) for pg in rd.pages) > 50 else "no"
            except Exception as e: pages2 = f"pypdf error {type(e).__name__}"
        cd = rr.headers.get("Content-Disposition", "")
        doc_rows.append(dict(meeting_id=mid, document_id=did, link=f"{BASE}/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID={did}", listed_title=d["title"], file_name=mm["file_name"],
            filename_header_second_fetch=cd, size=mm["size_bytes"], size_second_fetch=len(rr.content), sha256=mm["sha256"], sha256_second_fetch=sha2, sha_match=mm["sha256"] == sha2,
            pages_pdfinfo=mm["pages_or_slides"], pages_pypdf=pages2, pages_match=(str(pages2) == str(mm["pages_or_slides"])) if pages2 != "" else "n/a",
            text_poppler=mm["text_extracted"], text_pypdf=text2))
for fn, rs in ((f"../data/{TAG}_proof_sample_meetings.csv", rows), (f"../data/{TAG}_proof_sample_documents.csv", doc_rows)):
    with open(fn, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rs[0].keys())); w.writeheader(); w.writerows(rs)
print("meetings sampled", len(rows), {k: sum(1 for r in rows if r[k] is True or r[k] is False and False) for k in ("date_match", "requestor_match", "title_match", "docs_match", "attendees_match")})
print("docs sampled", len(doc_rows), "sha match", sum(d["sha_match"] for d in doc_rows), "pages match (pdf)", sum(1 for d in doc_rows if d["pages_match"] is True), "of", sum(1 for d in doc_rows if d["pages_match"] != "n/a"))
for r in rows:
    bad = [k for k in ("date_match", "requestor_match", "title_match", "docs_match", "attendees_match") if not r[k]]
    if bad: print("MISMATCH", r["meeting_id"], bad)
for d in doc_rows:
    if not d["sha_match"] or d["pages_match"] is False or d["text_poppler"] != ("yes" if d["text_pypdf"] in ("yes", "") else d["text_poppler"]): print("DOC DIFF", d["document_id"], d["sha_match"], d["pages_pdfinfo"], d["pages_pypdf"], d["text_poppler"], d["text_pypdf"])
