# Handoff

## What runs
`.github/workflows/refresh.yml`, Wednesdays 13:00 UTC. It re-reads the previous month and this month from reginfo.gov (1.6 seconds between requests, honest User-Agent, stops on 403/429), downloads that window's handouts, extracts text with poppler, merges into the Hugging Face dataset and uploads in one commit. No LLM.

## What you need
- A fork of this repo and a Hugging Face dataset to write to (change `REPO` in `scripts/refresh.py`).
- A repo secret `HF_TOKEN` with write access to that dataset. Nothing else.
- The explorer site is a config in the `dataset-explorer` repo (`configs/oira.json`); it reads the table from Hugging Face on page load.

## How it protects the data
The run stops without uploading if a month fails, if the collected meetings don't equal the site's own "records found" count, if the site returns nothing for a month we hold meetings for, if a handout's hash differs from its manifest, or if the merge would shrink the dataset.

## What breaks
- **reginfo.gov changes its pages.** The scrapers fail or the banner check fails; nothing is uploaded and GitHub emails you.
- **A meeting reginfo's search never returns** can't be caught; the checks compare the site to itself and to a second search by date range.
- **Meetings more than a month old are not re-read.** A late change to one of them (rescheduled, new handout) is missed. Run the backfill driver (`scripts/run_backfill.py`) to re-read older months.
- **Scanned handouts have no text.** No OCR is run.
