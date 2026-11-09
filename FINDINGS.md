# Findings: EO 12866 meetings and handouts, 2025-01-20 through 2026-11-08

Pulled from reginfo.gov on 2026-11-08, between about 18:05 and 19:46 Eastern. Range: every meeting the site's date-range search returns for 01/20/2025 through 11/08/2026, searched one calendar month at a time (2025-01 starts 01/20; 2026-11 ends 11/08). "Meeting date" is the date the site shows, so a meeting rescheduled later moves between months.

## Answer

- **Every month reconciled.** For all 23 months the site's own "Number Of Records Found" equals our count of distinct meeting ids, and a second count (the same range searched as 7-day sub-ranges: banners summed, ids unioned) agrees on both the number and the exact id set. No month disagrees. Per-month table: `data/monthly_reconciliation.csv` and the end of `PROOF.md`.
- **Totals:** 1,380 meetings (no meeting id appears in two months), 14,397 attendee rows, 1,371 document listings, all downloaded with HTTP 200 (none failed), 1,335 distinct SHA-256 hashes (36 listings are byte-identical copies of another listing, kept under each meeting), 1,628,954,390 bytes (about 1.63 GB) of handouts. Requests to reginfo.gov: 3,332 logged plus 2 early POSTs (403, CSRF; see prototype notes below), about 3,334 in total against the 4,500 budget. Statuses logged: 3,166 x 200, one 500, three connection drops that were retried. No 403 or 429 on any GET.
- **Two months have no meetings at all:** October 2025 and November 2025. The search page says "No results found for your search" for each (and for 01/20-01/31/2025), and the sub-range searches also find none. DataDawn also has none. I did not investigate why; this is what the site returns today. February 2025 has 1 meeting.
- **October 2026 re-verified:** the banner said 104 at 18:06 and again at 19:46; 104 ids both times, identical to the stored set. November 1-8 re-read at 19:46: 12; September 2026: 122.

## Spot check (a sample)

60 meetings across 17 months (50 random from all 1,380, seed 20261108, plus edge cases) were re-fetched live and compared field by field with a separately written parser: 60 of 60 match on date/time, requestor, requestor name, requestor client, title, document ids and titles, and attendee count. 36 of their documents were re-downloaded: SHA-256 identical for 36 of 36, PDF page counts agree between pdfinfo and pypdf. Attendee names were compared by count only. Details and links: `PROOF.md`.
Correction: my first run of this check reported 12 mismatches. They were my checker over-reading an adjacent field, not bad data; it did show that the CSVs lacked the page's "Requestor's Client" field, which I then added (`scripts/13_add_requestor_client.py`, re-parsed from saved HTML, no new requests) and the sample was re-run.

## Documents that did not extract cleanly (listed, not dropped)

All 1,371 are in the manifests (`data/<month>_document_manifest.csv`); 73 are not fully text-extracted, listed in `data/documents_not_fully_extracted.csv`: 67 with no text, 6 with very little. By file type: 49+5 PDFs (mostly scanned or image-only), 13 image files (7 png, 6 jpg), 3 docx, 1 pptx, 1 old-format .doc (not read), 1 PDF-named file with no extension. No OCR was run.
- Two listings (documents 1118292 and 1118293, meeting 1319273, month 2026-02) came back as HTTP 200 with zero bytes, twice (re-fetched). The site serves empty files for them.
- One PDF (1396392, meeting 1520823, 2026-09) is exactly 6,291,456 bytes (6 MiB), and poppler cannot parse it (no trailer). A re-fetch returned identical bytes, so it looks truncated at the source, not by our download. Not confirmed.
- 38 documents had no filename in the Content-Disposition header; their listed title is kept. Content type for the .png/.jpg/.doc files is reported by the server as `application/png` etc.; the manifest records what the server said.
Details: `data/bad_doc_recheck.json`.

## Comparison with DataDawn (counts only, for the range)

DataDawn's monthly counts equal ours in 17 of 23 months, including all twelve 2025 months (its empty Jan, Oct and Nov 2025 match the site's empty results). They differ for 2026-03 (91 vs our 88), 04 (90 vs 92), 05 (99 vs 98), 08 (102 vs 103), 10 (75 vs 104, stale snapshot) and 11 (0 vs 12). I did not redo the id-level comparison beyond October 2026 (below).

## Problems hit and fixes

- First backfill run died on 2025-11: the site returns no result page for an empty search, and my script did not handle "No results found" (the "view all" request then dropped the connection). Fixed, resumed from that month; earlier months were unaffected.
- Added retries (2, with a 15 s pause) for dropped connections; none were needed after that.
- The 2026-10 files in `data/` come from the prototype run, so they include the 10-per-page paginated pass and per-RIN check; other months use view-all plus the sub-range check only. For other months `*_search.json` has a partial `rows_paginated` list (first page only); ignore it, `rows_viewall` is the list.

## Caveats

- The checks cannot detect a meeting that reginfo's own search never returns, and statuses and dates change after the fact (rescheduled meetings leave a month; documents can be added to a meeting later). Counts are as of 2026-11-08, per month pulled at different times that evening.
- "Scheduled" in the status column does not mean future: seven October 2026 meetings dated before the pull still show Scheduled.
- Text extraction was checked for presence and page counts, not word for word. Office files are text-scraped from XML, so their page counts are blank.
- Handout contents were not read for meaning. Nothing downloaded is committed (`downloads/`, `raw/` are git-ignored).
- Resume: `cd scripts && ../.venv/bin/python run_backfill.py` skips months that have `data/<month>_DONE.json`. A new month needs adding to the range in `months()`.

---

# Prototype notes (October 2026, from the first slice)


Pulled from reginfo.gov on 2026-11-08 (about 17:30 to 17:50 Eastern). Covers meetings with a meeting date from 10/01/2026 through 10/31/2026 as the site's own date-range search returns them. Prototype on one month only.

## Answer

- **October reconciles.** Reginfo.gov's search says "Number Of Records Found: 104" for October 2026 when re-read on 2026-11-08 (17:43 ET). We have 104 distinct meeting ids. Three searches agree: view-all and the 10-per-page paginated pass return identical id sets, and five date sub-ranges sum to 104 with the same ids.
- **The backlog said 105, the site says 104 today.** The 105 was seen on 2026-11-01. We do not have the 11/01 list, so we cannot prove which meeting dropped out. One strong candidate: meeting 1528523 (RIN 0651-AD89, PTO, Final Rule Stage) is in DataDawn as 10/16/2026, is no longer in the October search, and its live page now shows 11/20/2026 (Scheduled). So it was rescheduled out of October. That explains a drop of one, but whether it was the one that moved between 11/01 and 11/08 is an inference.
- **Handouts: 99 documents on 56 of the 104 meeting pages, all downloaded (HTTP 200).** 99 distinct SHA-256 hashes, no duplicates, no repeated documentIDs across meetings. Text extracted for 98; 1 (document 1436342, meeting 1573623, 5 pages) is image-only. A quick OCR of its first page with tesseract read normal letter text, but OCR output was not saved and no OCR is in the pipeline.
- **It can scale**, but the full 2025-01-20 to now run would exceed the 1 GB disk budget (see Scaling). Not run.

## What is in `data/`

`2026-10_meetings.csv` (meeting id, RIN, date/time, agency, rule title, stage, status, requestor organization, requestor name, counts, URL), `2026-10_attendees.csv` (name, affiliation, participation mode, one row per attendee per meeting), `2026-10_documents_listed.csv` (what each meeting page lists), `2026-10_document_manifest.csv` (per document: meeting id, listed title, file name from the Content-Disposition header, content type, size, SHA-256, pages or slides, characters of text, extracted yes/no, note), `2026-10_downloads.json` (raw download log), check outputs, `2026-10_vs_datadawn.csv`, `request_log.jsonl`.

Meeting statuses as the site gives them: 96 Completed, 7 Scheduled, 1 No Show. The 7 "Scheduled" meetings are dated 10/05 to 10/30, all before the pull date, with no attendees or documents listed. The status is evidently not always updated after the date, so "Scheduled" does not mean future.

## Reconciliation checks (all on the full month, not a sample)

| check | result |
|---|---|
| Live banner vs our distinct ids | 104 vs 104 |
| View-all pass vs paginated pass (10 pages) | identical id sets |
| 5 weekly sub-range searches | banners sum 104; union of ids equals the month list |
| Boundaries: 09/30 and 11/01 | 1 meeting on 09/30, 0 on 11/01, neither in our list |
| Per-RIN search (27 RINs, no date filter, October rows counted) | 104, id sets equal for every RIN |
| EO review XML (under review + completed YTD) | all 27 RINs appear; XML has no meeting records, so plausibility only |

The per-RIN check can only see meetings on RINs that already appear in the month list, so on its own it cannot find a meeting missing from the month search. The sub-range search and the paginated pass use the same search engine as the banner, so none of these checks catches a meeting the site's search itself omits. We have no source independent of reginfo's search for meeting existence; the EO review XML does not list meetings.

## Spot check

20 meetings (8 random with documents, 3 random without, 9 deliberately chosen edge cases) and their 33 documents were re-checked against live pages with a separately written parser: date, requestor, title, document list, attendee count all matched for 20 of 20 after one false alarm (a title with a double space; the live HTML collapses whitespace, ours kept the original). All 33 second downloads had identical SHA-256. Page counts agreed between pdfinfo and pypdf for all 28 PDFs in the sample. Links in `PROOF.md`. This is a sample, not full verification. Attendee names and affiliations were only compared by count.

## DataDawn comparison (regs.datadawn.org, table `oira_meetings`, queried 2026-11-08)

Query used (Datasette JSON API, `_shape=array`): `select * from oira_meetings where meeting_date_iso>='2026-09-25' and meeting_date_iso<'2026-11-15'`.

DataDawn has 75 October meetings; we have 104. 74 are in both. 30 are only ours, 1 is only DataDawn's.
- **Only ours (30):** dated 10/13 to 10/30; DataDawn's latest meeting date anywhere is 10/29, so its October data stops before the end of the month and misses 6 meetings on 10/30 outright. The other 24 are earlier dates, consistent with meetings added after DataDawn's scrape, but we cannot tell when each was created. This matches issue #85's "recent months go stale".
- **Only DataDawn (1):** 1528523, rescheduled to 11/20 (above).
- **Status differences:** 47 of 74 shared meetings are "Completed" here and "Scheduled" in DataDawn (stale snapshot).
- **Date difference:** 1 shared meeting (1558573) is 10/26 here and 10/19 in DataDawn (rescheduled after its scrape; not independently confirmed).
- DataDawn's 2025 monthly counts have visible holes (no rows for 2025-01, 10, 11; 1 for Feb), so it should not be used as a backfill source. `data/datadawn_monthly_counts_since_2025-01-20.json`.

## Caveats and what was not verified

- Request count: 407 logged requests to reginfo.gov (one was a 500, the rest 200) plus 2 unlogged POSTs that returned 403 (CSRF, before switching to GET). About 410 in total; budget was 1,500. Disk used by downloads: 108 MB.
- We did not confirm that no meeting is missing from reginfo's own search.
- Text extraction was checked for presence and page counts only, not word-for-word against rendered pages. Office files are text-scraped from their XML, not rendered; page counts are not given for docx/xlsx.
- The "DataDawn only" explanation and the 105-to-104 explanation rest on one rescheduled meeting and are inferences.
- Handout contents were not read for meaning; some may be sensitive or copyrighted. Nothing downloaded is committed.
