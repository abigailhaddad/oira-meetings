"""Step 6 (more independent checks): (a) re-run the search over sub-ranges and compare union with the month search;
(b) check month RINs against OIRA's EO review XML (RIN-level data; it contains no meeting records, so this is plausibility only);
(c) re-read the live month 'Found: N' banner."""
import sys, re, csv, json, os
from bs4 import BeautifulSoup
from common import *
sys.path.insert(0, os.path.dirname(__file__))
TAG = sys.argv[1]
ranges = [("10/01/2026", "10/07/2026"), ("10/08/2026", "10/14/2026"), ("10/15/2026", "10/21/2026"), ("10/22/2026", "10/28/2026"), ("10/29/2026", "10/31/2026"),
          ("09/30/2026", "09/30/2026"), ("11/01/2026", "11/01/2026")]
def parse(h):
    s = BeautifulSoup(h, "lxml"); t = s.get_text(" ", strip=True); mm = re.search(r"Number Of Records Found:\s*(\d+)", t)
    ids = [re.search(r"meetingId=(\d+)", a["href"]).group(1) for a in s.find_all("a", href=re.compile(r"viewEO12866Meeting\?"))]
    dts = [a.get_text(" ", strip=True) for a in s.find_all("a", href=re.compile(r"viewEO12866Meeting\?"))]
    return (int(mm.group(1)) if mm else 0), ids, dts
res = []
for a, b in ranges:
    r = get(BASE + "/public/do/eom12866SearchResults", params={"searchStartDate": a, "searchEndDate": b, "operation": "", "resultCount": "1"})
    found, ids, dts = parse(r.text)
    if found > len(ids):
        r = get(BASE + "/public/do/eom12866SearchResults", params={"viewall": "y", "view": "yes", "viewAllFlag": "Y"}); f2, ids, dts = parse(r.text)
    res.append(dict(range=[a, b], found=found, ids=ids, dts=dts)); print(a, b, found, len(ids), flush=True)
mine = {m["meeting_id"] for m in csv.DictReader(open(f"../data/{TAG}_meetings.csv"))}
union = set(); [union.update(x["ids"]) for x in res[:5]]
chk = dict(sub_range_found_sum=sum(x["found"] for x in res[:5]), sub_range_union=len(union), month_ids=len(mine), union_eq_month=union == mine,
           in_union_not_month=sorted(union - mine), in_month_not_union=sorted(mine - union),
           boundary_sep30=res[5]["dts"], boundary_nov1=res[6]["dts"], ranges=res)
# live banner re-check
r = get(BASE + "/public/do/eom12866SearchResults", params={"searchStartDate": "10/01/2026", "searchEndDate": "10/31/2026", "operation": "", "resultCount": "1"})
chk["live_month_found_now"] = parse(r.text)[0]; chk["live_month_found_checked_at"] = time.strftime("%Y-%m-%d %H:%M:%S %Z")
# XML overlap
import xml.etree.ElementTree as ET
rins_m = {m["rin"] for m in csv.DictReader(open(f"../data/{TAG}_meetings.csv"))}
xml_rins = {}
for f in ["EO_RULES_UNDER_REVIEW", "EO_RULE_COMPLETED_YTD"]:
    root = ET.parse(f"../raw/{f}.xml").getroot()
    xml_rins[f] = {(x.findtext("RIN") or "").strip() for x in root.iter("REGACT")}
allx = set().union(*xml_rins.values())
chk["xml"] = dict(rins_in_month=len(rins_m), in_under_review=len(rins_m & xml_rins["EO_RULES_UNDER_REVIEW"]), in_completed_ytd=len(rins_m & xml_rins["EO_RULE_COMPLETED_YTD"]),
                  in_either=len(rins_m & allx), not_in_either=sorted(rins_m - allx), xml_rundate="2026-11-08")
json.dump(chk, open(f"../data/{TAG}_split_and_xml_check.json", "w"), indent=1)
print({k: v for k, v in chk.items() if k != "ranges"})
