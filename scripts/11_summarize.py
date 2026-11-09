"""Build data/monthly_reconciliation.csv and data/backfill_totals.json from per-month DONE files and manifests."""
import csv, glob, json, os, collections
tags = sorted(os.path.basename(f)[:7] for f in glob.glob("../data/*_DONE.json"))
rows = []; mt = dt = 0; hashes = set(); byt = 0; fails = []; notext = []; docs_total = 0; mids = set(); dup_mid = 0
for t in tags:
    d = json.load(open(f"../data/{t}_DONE.json"))
    ms = list(csv.DictReader(open(f"../data/{t}_meetings.csv"))); man = list(csv.DictReader(open(f"../data/{t}_document_manifest.csv")))
    for m in ms:
        if m["meeting_id"] in mids: dup_mid += 1
        mids.add(m["meeting_id"])
    for r in man:
        docs_total += 1
        if r["note"].startswith("DOWNLOAD FAILED"): fails.append((t, r["document_id"], r["note"])); continue
        hashes.add(r["sha256"]); byt += int(r["size_bytes"])
        if r["text_extracted"] != "yes": notext.append((t, r["document_id"], r["meeting_id"], r["file_name"], r["text_extracted"], r["note"].strip()))
    banner = d["banner"]; mine = len(ms); split = d.get("split_banner_sum")
    rows.append(dict(month=t, banner=banner, our_distinct_meeting_ids=mine, split_range_banner_sum=split, split_union_equals_ours=d.get("split_union_eq_month"),
                     all_three_agree=(banner == mine == split and d.get("split_union_eq_month") is True), docs_listed=len(man), requests=d.get("requests_this_month", "")))
with open("../data/monthly_reconciliation.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
tot = dict(months_done=len(tags), months=tags, meetings=len(mids), duplicate_meeting_ids_across_months=dup_mid, documents_listed=docs_total, distinct_sha256=len(hashes), bytes_downloaded_ok=byt,
           download_failures=fails, not_fully_text_extracted=notext, months_where_counts_disagree=[r["month"] for r in rows if not r["all_three_agree"]],
           requests_logged=sum(1 for _ in open("../data/request_log.jsonl")), status_counts=dict(collections.Counter(json.loads(l)["status"] for l in open("../data/request_log.jsonl"))))
json.dump(tot, open("../data/backfill_totals.json", "w"), indent=1)
print(json.dumps({k: v for k, v in tot.items() if k != "months"}, indent=1)[:3000])
