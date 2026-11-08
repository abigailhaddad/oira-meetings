# Findings: October 2026 prototype

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

## Scaling to 2025-01-20 through now (estimate, not run)

Measured this month: about 2.0 s per meeting page, about 4.0 s per document download (rate limit plus transfer), 0.95 documents per meeting, 1.05 MB per meeting (108.8 MB for 104 meetings; largest file 8.5 MB).

Meeting count is unknown. DataDawn shows 1,368 for the period (a lower bound given its holes); 2026 Jan to Oct alone is 907 per the backlog counts with October as 104. Planning range: 1,400 to 2,000 meetings.
- Requests: about 1 per meeting page + 1 per document + 2 per month listing: 2,700 to 3,900. The 1,500-request budget would not cover it. Add about 1 more per RIN-month if the per-RIN check is repeated.
- Time at 1.6 s minimum gap: about 2.3 to 3.3 hours if run continuously.
- Disk: about 1.5 to 2.1 GB of handouts, over the 1 GB budget. Text and metadata are small (this month: 0.7 MB in `data/`).
- Failure modes seen or likely: (1) POST to the search form returns 403 (Tomcat CSRF) without a matching session token; GET with query parameters works and is what the scripts use. (2) Search results are server-side session state: "view all" only works right after the search in the same session, and the paginated parameter `pagenum` is 0-based (an off-by-one skipped a page in our first run; the page past the end returned HTTP 500). (3) Searches are capped near 1,000 results (per DataDawn issue #85, not tested here), so keep to month-sized windows (max seen in 2026 is 122). (4) Status, date and document list change after the fact (rescheduling moves meetings out of a month; documents may be added later), so a month is not final until later; re-pull trailing months. (5) Two PDFs came without a filename header (the meeting page title is kept instead). One quoted filename contained a semicolon and was truncated by an early version of the parser; found in review, fixed, and the manifest rebuilt. (6) Image-only PDFs; no OCR in the pipeline. (7) Reginfo is a small team's site; stop on any 403/429.

## Caveats and what was not verified

- Request count: 407 logged requests to reginfo.gov (one was a 500, the rest 200) plus 2 unlogged POSTs that returned 403 (CSRF, before switching to GET). About 410 in total; budget was 1,500. Disk used by downloads: 108 MB.
- We did not confirm that no meeting is missing from reginfo's own search.
- Text extraction was checked for presence and page counts only, not word-for-word against rendered pages. Office files are text-scraped from their XML, not rendered; page counts are not given for docx/xlsx.
- The "DataDawn only" explanation and the 105-to-104 explanation rest on one rescheduled meeting and are inferences.
- Handout contents were not read for meaning; some may be sensitive or copyrighted. Nothing downloaded is committed.
