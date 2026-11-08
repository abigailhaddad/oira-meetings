"""Step 9: render PROOF.md from the proof-sample CSVs and check JSONs."""
import sys, csv, json
TAG = sys.argv[1]
M = list(csv.DictReader(open(f"../data/{TAG}_proof_sample_meetings.csv"))); D = list(csv.DictReader(open(f"../data/{TAG}_proof_sample_documents.csv")))
MAN = {r["document_id"]: r for r in csv.DictReader(open(f"../data/{TAG}_document_manifest.csv"))}
for d in D: d["file_name"] = MAN[d["document_id"]]["file_name"]  # current manifest is authoritative for names
S = json.load(open(f"../data/{TAG}_split_and_xml_check.json")); R = json.load(open(f"../data/{TAG}_per_rin_check.json"))
o = ["# Proof file: spot-check against the live site", "",
     f"Sample of {len(M)} meetings and {len(D)} documents from {TAG}, drawn with `random.seed(20261108)` (8 random meetings that have documents, 3 random meetings with none) plus deliberately chosen edge cases (the `why` column). This is a SAMPLE, not a full verification.",
     "Method: each meeting page was fetched a second time and parsed with a separately written regex parser (the main scripts use BeautifulSoup); each document was downloaded a second time and its SHA-256 compared; page counts compared between poppler `pdfinfo` and `pypdf`.", "",
     "## Meetings (our saved value vs. live page re-fetched)", "", "| meeting | why sampled | date ours / live | requestor ours / live | docs ours / live | attendees ours / live | all match |", "|---|---|---|---|---|---|---|"]
for r in M:
    ok = all(r[k] == "True" for k in ("date_match", "requestor_match", "title_match", "docs_match", "attendees_match"))
    o.append(f"| [{r['meeting_id']}]({r['link']}) | {r['why']} | {r['date_ours']} / {r['date_live']} | {r['requestor_ours']} / {r['requestor_live']} | {r['docs_ours']} / {r['docs_live']} | {r['attendees_ours']} / {r['attendees_live']} | {'yes' if ok else 'NO'} |")
o += ["", "## Documents (first download vs. second download)", "", "| document | meeting | file name | size | SHA-256 (first 12) | second-fetch SHA matches | pages pdfinfo / pypdf | text poppler / pypdf |", "|---|---|---|---|---|---|---|---|"]
for d in D:
    o.append(f"| [{d['document_id']}]({d['link']}) | {d['meeting_id']} | {d['file_name'] or '(no filename header; title: ' + d['listed_title'] + ')'} | {d['size']} | {d['sha256'][:12]} | {d['sha_match']} | {d['pages_pdfinfo']} / {d['pages_pypdf']} | {d['text_poppler']} / {d['text_pypdf'] or 'n/a'} |")
o += ["", "## Count reconciliation (full month, not a sample)", "",
      f"- Live banner 'Number Of Records Found' re-read at {S['live_month_found_checked_at']}: {S['live_month_found_now']}.",
      f"- Our month list: {S['month_ids']} unique meeting ids (view-all pass and 10-per-page paginated pass returned identical id sets).",
      f"- Same search split into 5 date sub-ranges: banners sum to {S['sub_range_found_sum']}, union of ids = {S['sub_range_union']}, identical to the month list: {S['union_eq_month']}. Day before (09/30) and day after (11/01) boundary checks returned {len(S['boundary_sep30'])} and {len(S['boundary_nov1'])} meetings (outside the month).",
      f"- Per-RIN cross-check ({len(R['results'])} RINs, searched with no date filter, October rows counted): {sum(x['per_rin_count'] for x in R['results'])} meetings, id sets equal for every RIN: {all(x['match'] for x in R['results'])}. Limit: this can only find meetings on RINs already in the month list.",
      f"- EO review XML (rules under review + completed YTD, RUNDATE {S['xml']['xml_rundate']}): {S['xml']['in_either']} of {S['xml']['rins_in_month']} month RINs appear. The XML has no meeting records, so this is plausibility only, not a count check."]
open("../PROOF.md", "w").write("\n".join(o) + "\n"); print("wrote PROOF.md")
