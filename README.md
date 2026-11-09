# oira-meetings

Archive builder for Executive Order 12866 meetings held at OIRA, from reginfo.gov: one metadata row per meeting, the list of attendees, and the handout documents attached to each meeting page. Run one month at a time, or over a range with `scripts/run_backfill.py`.

Not affiliated with OMB, OIRA, GSA or reginfo.gov. It reads public pages only. It is slow on purpose (at least 1.6 seconds between requests, honest User-Agent) and stops on any 403 or 429.

## Run

Needs Python 3, `pdftotext` and `pdfinfo` (poppler).

    python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
    cd scripts
    ../.venv/bin/python 01_list_month.py 10/01/2026 10/31/2026 2026-10   # month search -> data/2026-10_search.json
    ../.venv/bin/python 02_fetch_meetings.py 2026-10                    # meeting pages -> meetings / attendees / documents CSVs
    ../.venv/bin/python 03_download_docs.py 2026-10                     # handouts -> downloads/ (not committed)
    ../.venv/bin/python -I 05_extract_text.py 2026-10                   # hashes, pages, text -> document manifest
    ../.venv/bin/python 04_per_rin_check.py 2026-10 2026 10             # check 1: per-RIN search
    ../.venv/bin/python 06_split_range_and_xml_check.py 2026-10         # check 2: date sub-ranges, EO review XML, live banner
    ../.venv/bin/python 07_compare_datadawn.py 2026-10 2026 10          # comparison with DataDawn
    ../.venv/bin/python 08_spot_check.py 2026-10                        # re-fetch a random sample
    ../.venv/bin/python 09_make_proof.py 2026-10                        # writes PROOF.md

Step 07 reads `data/datadawn_2026-10_window.json`, a pull from the public DataDawn Datasette (`regs.datadawn.org/openregs`, table `oira_meetings`); see the query in FINDINGS.md.

## Layout

- `scripts/` the pipeline. `common.py` holds the rate limiter and request log.
- `data/` generated outputs for the month: meetings, attendees, documents listed, document manifest (size, SHA-256, pages, text extracted), reconciliation checks, DataDawn comparison, request log.
- `downloads/` and `raw/` hold the downloaded handouts and saved HTML. They are untrusted input and are git-ignored. Read them only with `python -I` or poppler tools.
- `FINDINGS.md` results and caveats. `PROOF.md` the spot-check sample with links.

All numbers live in `data/`, `FINDINGS.md` and `PROOF.md`, not here.

Full-range run: `cd scripts && ../.venv/bin/python run_backfill.py` (resumable; skips months with a `data/<month>_DONE.json`), then `11_summarize.py`, `12_recheck_bad_docs.py`, `10_final_spot_check.py`, `13_add_requestor_client.py`, `14_proof_final_section.py`.
