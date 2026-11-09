"""Add requestor_client to each month's meetings CSV by re-parsing the saved raw meeting HTML (no network)."""
import csv, glob, os, re, html
def txt(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s)).replace("\xa0", " ")).strip()
for f in sorted(glob.glob("../data/20??-??_meetings.csv")):
    tag = os.path.basename(f)[:7]; rows = list(csv.DictReader(open(f)))
    if not rows or "requestor_client" in rows[0]: continue
    for r in rows:
        h = open(f"../raw/{tag}/meetings/{r['meeting_id']}.html").read()
        m = re.search(r"for=requestorClient>.*?</label>(.*?)(?:<label|</p>)", h, re.S)
        r["requestor_client"] = txt(m.group(1)) if m else ""
    with open(f, "w", newline="") as o:
        w = csv.DictWriter(o, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(tag, len(rows), "with client:", sum(1 for r in rows if r["requestor_client"]))
