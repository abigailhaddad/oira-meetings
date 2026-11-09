"""Step 1: list EO 12866 meetings for a month from reginfo.gov search (view-all, plus a paginated second pass)."""
import sys, re, csv, json, os
from bs4 import BeautifulSoup
from common import *
START, END = sys.argv[1], sys.argv[2]   # MM/DD/YYYY
TAG = sys.argv[3]
RAW = f"../raw/{TAG}"; os.makedirs(RAW, exist_ok=True)

def parse(html):
    s = BeautifulSoup(html, "lxml")
    t = s.get_text(" ", strip=True)
    m = re.search(r"Number Of Records Found:\s*(\d+)", t)
    found = int(m.group(1)) if m else None
    rows = []
    for a in s.find_all("a", href=re.compile(r"viewEO12866Meeting\?")):
        tr = a.find_parent("tr")
        tds = [td.get_text(" ", strip=True) for td in tr.find_all("td", recursive=False)]
        q = re.search(r"rin=([^&]+)&meetingId=(\d+)", a["href"])
        rows.append(dict(meeting_id=q.group(2), rin=q.group(1), meeting_datetime=tds[0], agency=tds[2],
                         rule_title=tds[3], stage=tds[4], meeting_type=tds[5], href=a["href"]))
    return found, rows

r = get(BASE + "/public/do/eom12866SearchResults", params={"searchStartDate": START, "searchEndDate": END, "operation": "", "resultCount": "1"})
open(f"{RAW}/search_page1.html", "w").write(r.text)
found1, rows_p1 = parse(r.text)
if found1 is None and "No results found" in BeautifulSoup(r.text, "lxml").get_text(" ", strip=True):
    found1 = 0   # site says "No results found for your search"
    json.dump(dict(found_banner=0, note="site page says No results found", pulled=time.strftime("%Y-%m-%d %H:%M:%S %Z"), rows_viewall=[], rows_paginated=[]), open(f"../data/{TAG}_search.json", "w"), indent=1)
    print("no results"); sys.exit(0)
# pass A: view all
r = get(BASE + "/public/do/eom12866SearchResults", params={"viewall": "y", "view": "yes", "viewAllFlag": "Y"})
open(f"{RAW}/search_viewall.html", "w").write(r.text)
foundA, rowsA = parse(r.text)
# pass B: paginated (10/page)
NOPAGE = len(sys.argv) > 4 and sys.argv[4] == "nopage"
rowsB = list(rows_p1); n = 0   # pagenum is 0-based: first "Next" link is pagenum=1
while not NOPAGE and len(rowsB) < found1:
    n += 1
    r = get(BASE + "/public/do/eom12866SearchResults", params={"view": "yes", "pagenum": str(n)})
    open(f"{RAW}/search_page{n+1}.html", "w").write(r.text)
    f, rws = parse(r.text)
    if not rws: break
    rowsB += rws
    if n > 40: break
print("found banner:", found1, foundA, "| viewall rows", len(rowsA), "unique ids", len({x['meeting_id'] for x in rowsA}),
      "| paginated rows", len(rowsB), "unique ids", len({x['meeting_id'] for x in rowsB}), "pages", n)
print("viewall==paginated id sets:", {x['meeting_id'] for x in rowsA} == {x['meeting_id'] for x in rowsB})
json.dump(dict(found_banner=found1, pulled=time.strftime("%Y-%m-%d %H:%M:%S %Z"), rows_viewall=rowsA, rows_paginated=rowsB), open(f"../data/{TAG}_search.json", "w"), indent=1)
