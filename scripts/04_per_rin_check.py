"""Step 4 (independent reconciliation): for each RIN seen in the month, ask reginfo for all meetings on that RIN (rin search, no date filter),
count those whose date falls in the month, compare to the month search."""
import sys, re, csv, json, os
from bs4 import BeautifulSoup
from common import *
TAG, Y, M = sys.argv[1], sys.argv[2], sys.argv[3]
RAW = f"../raw/{TAG}/per_rin"; os.makedirs(RAW, exist_ok=True)
meet = list(csv.DictReader(open(f"../data/{TAG}_meetings.csv")))
rins = sorted({m["rin"] for m in meet})
def parse(h):
    s = BeautifulSoup(h, "lxml"); rows = []
    t = s.get_text(" ", strip=True); mm = re.search(r"Number Of Records Found:\s*(\d+)", t)
    for a in s.find_all("a", href=re.compile(r"viewEO12866Meeting\?")):
        tds = [td.get_text(" ", strip=True) for td in a.find_parent("tr").find_all("td", recursive=False)]
        q = re.search(r"rin=([^&]+)&meetingId=(\d+)", a["href"])
        rows.append(dict(meeting_id=q.group(2), rin=q.group(1), dt=tds[0]))
    return (int(mm.group(1)) if mm else None), rows
out = {}
for rin in rins:
    r = get(BASE + "/public/do/eom12866SearchResults", params={"rin": rin, "viewRule": "true", "operation": "", "resultCount": "1"})
    found, rows = parse(r.text)
    if found is not None and len(rows) < found:
        r = get(BASE + "/public/do/eom12866SearchResults", params={"viewall": "y", "view": "yes", "viewAllFlag": "Y"})
        found2, rows = parse(r.text)
    open(f"{RAW}/{rin}.html", "w").write(r.text)
    inmonth = [x for x in rows if x["dt"][6:10] == Y and x["dt"][0:2] == M]
    out[rin] = dict(found_all_time=found, rows_parsed=len(rows), unique_ids=len({x['meeting_id'] for x in rows}), in_month_ids=sorted(x["meeting_id"] for x in inmonth))
    print(rin, found, len(rows), len(inmonth), flush=True)
mine = {}
for m in meet: mine.setdefault(m["rin"], set()).add(m["meeting_id"])
res = []
for rin in rins:
    res.append(dict(rin=rin, month_search_count=len(mine[rin]), per_rin_count=len(out[rin]["in_month_ids"]), match=set(out[rin]["in_month_ids"]) == mine[rin],
                    only_in_month_search=sorted(mine[rin] - set(out[rin]["in_month_ids"])), only_in_per_rin=sorted(set(out[rin]["in_month_ids"]) - mine[rin]), per_rin_found_all_time=out[rin]["found_all_time"], per_rin_rows_parsed=out[rin]["rows_parsed"]))
json.dump(dict(pulled=time.strftime("%Y-%m-%d %H:%M:%S %Z"), results=res), open(f"../data/{TAG}_per_rin_check.json", "w"), indent=1)
print("total month search", sum(r["month_search_count"] for r in res), "total per-rin", sum(r["per_rin_count"] for r in res), "all match", all(r["match"] for r in res))
