"""Step 2: fetch each meeting page listed in data/<TAG>_search.json, parse metadata, attendees, documents."""
import sys, re, csv, json, os, html
from bs4 import BeautifulSoup
from common import *
TAG = sys.argv[1]
RAW = f"../raw/{TAG}/meetings"; os.makedirs(RAW, exist_ok=True)
search = json.load(open(f"../data/{TAG}_search.json"))
rows = search["rows_viewall"]

def parse_meeting(h):
    s = BeautifulSoup(h, "lxml")
    out = {}
    for lab in s.find_all("label"):
        k = (lab.get("for") or "").strip()
        if k in ("ruleTitle", "agencySubAgencyAcronym", "ruleStageDesc", "meetingDate", "requestor", "requestorName"):
            # value = text following the label up to next label / end of paragraph
            txt = ""
            for sib in lab.next_siblings:
                if getattr(sib, "name", None) == "label": break
                txt += sib.get_text(" ") if hasattr(sib, "get_text") else str(sib)
            out[k] = re.sub(r"\s+", " ", txt.replace("\xa0", " ")).strip()
    docs = []
    for b in s.find_all("button", class_="downloadLinkBtn"):
        m = re.search(r"documentID=(\d+)", b.get("onclick", ""))
        docs.append(dict(document_id=m.group(1) if m else None, title=b.get_text(" ", strip=True)))
    att = []
    t = [x for x in s.find_all("table") if "List of EO 12866 Meetings Attendees" in (x.get("summary") or "")]
    if t:
        for tr in t[0].find_all("tr"):
            tds = [td.get_text(" ", strip=True).replace("\xa0", " ") for td in tr.find_all("td")]
            if len(tds) == 3:
                nm = re.sub(r"\s+", " ", tds[1]).strip()
                part = tds[2].strip()
                name, _, aff = nm.partition(" - ")
                att.append(dict(name=name.strip(), affiliation=aff.strip(), participation=part))
    return out, docs, att

meetings, docrows, attrows, fails = [], [], [], []
for i, r in enumerate(rows):
    fn = f"{RAW}/{r['meeting_id']}.html"
    if os.path.exists(fn): h = open(fn).read()
    else:
        try:
            resp = get(BASE + "/public/do/viewEO12866Meeting", params={"viewRule": "false", "rin": r["rin"], "meetingId": r["meeting_id"], "acronym": r["agency"]})
        except Blocked as e:
            print("BLOCKED", e); sys.exit(2)
        except requests.RequestException as e:
            fails.append((r["meeting_id"], f"exception {type(e).__name__}")); continue
        if resp.status_code != 200: fails.append((r["meeting_id"], resp.status_code)); continue
        h = resp.text; open(fn, "w").write(h)
    meta, docs, att = parse_meeting(h)
    meetings.append(dict(meeting_id=r["meeting_id"], rin=r["rin"], meeting_datetime=meta.get("meetingDate") or r["meeting_datetime"],
        list_meeting_datetime=r["meeting_datetime"], agency=meta.get("agencySubAgencyAcronym") or r["agency"], rule_title=meta.get("ruleTitle") or r["rule_title"],
        stage=meta.get("ruleStageDesc") or r["stage"], meeting_type=r["meeting_type"], requestor=meta.get("requestor", ""), requestor_name=meta.get("requestorName", ""),
        n_documents=len(docs), n_attendees=len(att), url=BASE + "/public/do/viewEO12866Meeting?" + r["href"].split("?")[1]))
    for d in docs: docrows.append(dict(meeting_id=r["meeting_id"], **d))
    for a in att: attrows.append(dict(meeting_id=r["meeting_id"], **a))
    if i % 20 == 0: print(i, flush=True)

def wcsv(fn, rs, fields):
    with open(fn, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rs)
MF = ["meeting_id","rin","meeting_datetime","list_meeting_datetime","agency","rule_title","stage","meeting_type","requestor","requestor_name","n_documents","n_attendees","url"]
wcsv(f"../data/{TAG}_meetings.csv", meetings, MF); wcsv(f"../data/{TAG}_documents_listed.csv", docrows, ["meeting_id","document_id","title"]); wcsv(f"../data/{TAG}_attendees.csv", attrows, ["meeting_id","name","affiliation","participation"])
json.dump(dict(pulled=time.strftime("%Y-%m-%d %H:%M:%S %Z"), meetings=meetings, documents=docrows, attendees=attrows, fetch_failures=fails), open(f"../data/{TAG}_meetings.json", "w"), indent=1)
print("meetings", len(meetings), "docs", len(docrows), "attendee rows", len(attrows), "fails", fails)
