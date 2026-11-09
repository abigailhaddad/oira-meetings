"""Append the full-range spot-check section and the per-month reconciliation table to PROOF.md (idempotent)."""
import csv, json
M = list(csv.DictReader(open("../data/final_proof_sample_meetings.csv"))); D = list(csv.DictReader(open("../data/final_proof_sample_documents.csv")))
R = list(csv.DictReader(open("../data/monthly_reconciliation.csv")))
p = open("../PROOF.md").read().split("\n# Full-range proof")[0].rstrip() + "\n"
ks = ("date_match", "requestor_match", "reqname_match", "client_match", "title_match", "docs_match", "attendees_match")
o = ["", "# Full-range proof (2025-01-20 through 2026-11-08)", "",
     f"Sample of {len(M)} meetings drawn with `random.seed(20261108)` from all {sum(int(r['our_distinct_meeting_ids']) for r in R)} stored meetings (50 random plus edge cases: no extracted text, no filename header, each file type present, most documents, Scheduled / No Show status, earliest and latest month), covering {len({m['month'] for m in M})} months. Each was re-fetched live and compared field by field (date/time, requestor, requestor name, requestor client, title, document ids and titles, attendee count) with a separately written regex parser. This is a SAMPLE.",
     f"Result: {sum(all(m[k] == 'True' for k in ks) for m in M)} of {len(M)} meetings match on every field. (A first run showed 12 requestor-name mismatches; the cause was my checker over-capturing the adjacent 'Requestor's Client' field, and it also exposed that the stored CSV lacked that field. I fixed the checker, added `requestor_client` to the CSVs by re-parsing saved HTML, and re-ran: 60 of 60.)",
     f"Documents: {len(D)} of their documents were downloaded a second time; SHA-256 identical for {sum(d['sha_match'] == 'True' for d in D)} of {len(D)}; PDF page counts agree between pdfinfo and pypdf for {sum(d['pages_match'] == 'True' for d in D)} of {sum(d['pages_match'] != 'n/a' for d in D)} PDFs checked.", "",
     "| meeting | month | why sampled | date | requestor | name | client | docs ours/live | attendees ours/live | all match |", "|---|---|---|---|---|---|---|---|---|---|"]
for m in M:
    o.append(f"| [{m['meeting_id']}]({m['link']}) | {m['month']} | {m['why']} | {m['date_live']} | {m['requestor_live'][:40]} | {m['requestor_name_live']} | {m['client_live'][:30]} | {m['docs_ours']}/{m['docs_live']} | {m['attendees_ours']}/{m['attendees_live']} | {'yes' if all(m[k] == 'True' for k in ks) else 'NO'} |")
o += ["", "## Documents re-downloaded", "", "| document | meeting | file name | size | SHA-256 (12) | match | pages pdfinfo/pypdf |", "|---|---|---|---|---|---|---|"]
for d in D: o.append(f"| [{d['document_id']}]({d['link']}) | {d['meeting_id']} | {d['file_name'] or '(none)'} | {d['size']} | {d['sha256'][:12]} | {d['sha_match']} | {d['pages_pdfinfo']}/{d['pages_pypdf']} |")
o += ["", "## Per-month banner vs ours vs second count", "", "Banner = site's 'Number Of Records Found' for that month's date range (2025-01 starts 01/20; 2026-11 ends 11/08). Second count = the same range searched as 7-day sub-ranges, banners summed and ids unioned. Also in `data/monthly_reconciliation.csv`.", "",
      "| month | banner | ours (distinct ids) | sub-range sum | union equals ours | documents listed |", "|---|---|---|---|---|---|"]
for r in R: o.append(f"| {r['month']} | {r['banner']} | {r['our_distinct_meeting_ids']} | {r['split_range_banner_sum']} | {r['split_union_equals_ours']} | {r['docs_listed']} |")
open("../PROOF.md", "w").write(p + "\n".join(o) + "\n"); print("ok")
