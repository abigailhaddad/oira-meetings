"""Final spot check across all finished months: re-fetch a random sample of meetings (>=40) plus edge cases, compare field by field with stored data using
the independent regex parser; re-download a subset of their documents and compare SHA-256. Writes data/final_proof_sample_{meetings,documents}.csv."""
import logging; logging.disable(logging.CRITICAL)
import sys, csv, glob, json, os, re, random, hashlib, html
from common import *
from pypdf import PdfReader
N_MEET = int(sys.argv[1]) if len(sys.argv) > 1 else 45; MAX_DOCS = int(sys.argv[2]) if len(sys.argv) > 2 else 30
tags = sorted(os.path.basename(f)[:7] for f in glob.glob("../data/*_DONE.json"))
meet, docs, man = {}, [], {}
for t in tags:
    for m in csv.DictReader(open(f"../data/{t}_meetings.csv")): m["tag"] = t; meet[m["meeting_id"]] = m
    docs += list(csv.DictReader(open(f"../data/{t}_documents_listed.csv")))
    man.update({d["document_id"]: d for d in csv.DictReader(open(f"../data/{t}_document_manifest.csv"))})
bymeet = {}
for d in docs: bymeet.setdefault(d["meeting_id"], []).append(d)
random.seed(20261108)
ids = sorted(meet)
sample = {m: "random" for m in random.sample(ids, N_MEET)}
def edge(label, pred):
    c = [m for m in ids if pred(m) and m not in sample]
    if c: sample[random.choice(c)] = label
edge("edge: no text extracted", lambda m: any(man[d["document_id"]]["text_extracted"] == "no" for d in bymeet.get(m, [])))
edge("edge: no filename header", lambda m: any(not man[d["document_id"]]["file_name"] for d in bymeet.get(m, [])))
for ext in ("pptx", "docx", "xlsx", "doc", "xls", "zip"):
    edge(f"edge: {ext}", lambda m, ext=ext: any(man[d["document_id"]]["file_name"].lower().endswith("." + ext) for d in bymeet.get(m, [])))
edge("edge: most documents", lambda m: len(bymeet.get(m, [])) == max(len(v) for v in bymeet.values()))
for st in ("Scheduled", "No Show", "Cancelled"): edge(f"edge: status {st}", lambda m, st=st: meet[m]["meeting_type"] == st)
first_tag, last_tag = tags[0], tags[-1]
edge(f"edge: earliest month", lambda m: meet[m]["tag"] == first_tag); edge("edge: latest month", lambda m: meet[m]["tag"] == last_tag)
def txt(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s)).replace("\xa0", " ")).strip()
rows, doc_rows = [], []
for mid, why in sample.items():
    m = meet[mid]
    h = get(BASE + "/public/do/viewEO12866Meeting", params={"viewRule": "false", "rin": m["rin"], "meetingId": mid, "acronym": m["agency"]}).text
    g = lambda pat: (re.search(pat, h, re.S).group(1) if re.search(pat, h, re.S) else "")
    live_dt = txt(g(r"for=meetingDate>.*?</label>(.*?)</p>")); live_rq = txt(g(r"for=requestor>.*?</label>(.*?)<label")); live_title = txt(g(r"for=\"ruleTitle\">.*?</label>(.*?)</p>"))
    live_rn = txt(g(r"for=requestorName>.*?</label>(.*?)(?:<label|</p>)")); live_cl = txt(g(r"for=requestorClient>.*?</label>(.*?)(?:<label|</p>)"))
    live_docs = [(i, txt(t)) for i, t in re.findall(r"documentID=(\d+)\"\)'>\s*(.*?)\s*</button>", h, re.S)]
    live_att = len(re.findall(r'<td align="right" valign="bottom" style="width: 25px">', h))
    n = lambda x: re.sub(r"\s+", " ", x or "").strip()
    ours_docs = [(d["document_id"], n(d["title"])) for d in bymeet.get(mid, [])]
    rows.append(dict(meeting_id=mid, month=m["tag"], why=why, link=f"{BASE}/public/do/viewEO12866Meeting?viewRule=false&rin={m['rin']}&meetingId={mid}",
        date_ours=m["meeting_datetime"], date_live=live_dt, date_match=m["meeting_datetime"] == live_dt, requestor_ours=m["requestor"], requestor_live=live_rq, requestor_match=n(m["requestor"]) == live_rq,
        reqname_match=n(m["requestor_name"]) == live_rn, requestor_name_live=live_rn, client_ours=m.get("requestor_client", ""), client_live=live_cl, client_match=n(m.get("requestor_client", "")) == live_cl, title_match=n(m["rule_title"]) == live_title, docs_ours=len(ours_docs), docs_live=len(live_docs), docs_match=ours_docs == live_docs,
        attendees_ours=int(m["n_attendees"]), attendees_live=live_att, attendees_match=int(m["n_attendees"]) == live_att))
# documents: all docs of edge-case meetings first, then docs of random meetings until MAX_DOCS
cand = [d for mid in sample for d in bymeet.get(mid, [])]
cand.sort(key=lambda d: (not sample[d["meeting_id"]].startswith("edge"), d["document_id"])); cand = cand[:MAX_DOCS]
for d in cand:
    did = d["document_id"]; mm = man[did]
    if mm["note"].startswith("DOWNLOAD FAILED"): continue
    rr = get(BASE + "/public/do/eoDownloadDocument", params={"pubId": "", "eodoc": "true", "documentID": did})
    sha2 = hashlib.sha256(rr.content).hexdigest(); pages2 = ""
    p = f"../downloads/{d['meeting_id'] and meet[d['meeting_id']]['tag']}/{did}.bin"
    if mm["content_type"] == "application/pdf":
        try: rd = PdfReader(p); pages2 = len(rd.pages)
        except Exception as e: pages2 = f"pypdf error {type(e).__name__}"
    doc_rows.append(dict(meeting_id=d["meeting_id"], document_id=did, link=f"{BASE}/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID={did}", file_name=mm["file_name"], size=mm["size_bytes"], size_second_fetch=len(rr.content),
        sha256=mm["sha256"], sha256_second_fetch=sha2, sha_match=mm["sha256"] == sha2, pages_pdfinfo=mm["pages_or_slides"], pages_pypdf=pages2, pages_match=(str(pages2) == str(mm["pages_or_slides"])) if pages2 != "" else "n/a"))
for fn, rs in (("../data/final_proof_sample_meetings.csv", rows), ("../data/final_proof_sample_documents.csv", doc_rows)):
    if not rs: continue
    with open(fn, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rs[0].keys())); w.writeheader(); w.writerows(rs)
ks = ("date_match", "requestor_match", "reqname_match", "client_match", "title_match", "docs_match", "attendees_match")
print("meetings", len(rows), "all fields match:", sum(all(r[k] for k in ks) for r in rows), "| docs", len(doc_rows), "sha ok", sum(d["sha_match"] for d in doc_rows), "| months covered", len({r["month"] for r in rows}))
for r in rows:
    bad = [k for k in ks if not r[k]]
    if bad: print("MISMATCH", r["meeting_id"], r["month"], bad, r["date_ours"], r["date_live"])
for d in doc_rows:
    if not d["sha_match"] or d["pages_match"] is False: print("DOC DIFF", d["document_id"])
