"""Step 7: compare our month list with DataDawn's oira_meetings (pulled from regs.datadawn.org Datasette; file data/datadawn_<TAG>_window.json)."""
import sys, csv, json, collections
TAG = sys.argv[1]; Y, M = sys.argv[2], sys.argv[3]
ours = {m["meeting_id"]: m for m in csv.DictReader(open(f"../data/{TAG}_meetings.csv"))}
dd_all = json.load(open(f"../data/datadawn_{TAG}_window.json"))
dd = {x["meeting_id"]: x for x in dd_all if x["meeting_date_iso"].startswith(f"{Y}-{M}")}
def iso(s): return f"{s[6:10]}-{s[0:2]}-{s[3:5]}"
both = set(ours) & set(dd); only_o = set(ours) - set(dd); only_d = set(dd) - set(ours)
rows = []
for i in sorted(ours, key=lambda k: iso(ours[k]["meeting_datetime"])):
    o = ours[i]
    rows.append(dict(meeting_id=i, in_ours="yes", in_datadawn="yes" if i in dd else "no", date=iso(o["meeting_datetime"]), rin=o["rin"], agency=o["agency"], our_status=o["meeting_type"],
                     dd_status=dd[i]["meeting_type"] if i in dd else "", dd_date=dd[i]["meeting_date_iso"] if i in dd else ""))
for i in sorted(only_d):
    rows.append(dict(meeting_id=i, in_ours="no", in_datadawn="yes", date=dd[i]["meeting_date_iso"], rin=dd[i]["rin"], agency=dd[i]["agency_acronym"], our_status="", dd_status=dd[i]["meeting_type"], dd_date=dd[i]["meeting_date_iso"]))
with open(f"../data/{TAG}_vs_datadawn.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
mis = [(i, ours[i]["meeting_type"], dd[i]["meeting_type"]) for i in both if ours[i]["meeting_type"] != dd[i]["meeting_type"]]
dmis = [(i, iso(ours[i]["meeting_datetime"]), dd[i]["meeting_date_iso"]) for i in both if iso(ours[i]["meeting_datetime"]) != dd[i]["meeting_date_iso"]]
od = sorted(iso(ours[i]["meeting_datetime"]) for i in only_o)
summ = dict(ours=len(ours), datadawn=len(dd), both=len(both), only_ours=len(only_o), only_datadawn=len(only_d), only_datadawn_ids=sorted(only_d),
            only_ours_date_min=od[0] if od else None, only_ours_date_max=od[-1] if od else None, only_ours_by_date=dict(collections.Counter(od)),
            datadawn_max_date_in_window=max(x["meeting_date_iso"] for x in dd_all), datadawn_sources=dict(collections.Counter(x["source"] for x in dd.values())),
            status_mismatches=mis, date_mismatches=dmis)
json.dump(summ, open(f"../data/{TAG}_vs_datadawn_summary.json", "w"), indent=1); print(json.dumps(summ, indent=1)[:2500])
