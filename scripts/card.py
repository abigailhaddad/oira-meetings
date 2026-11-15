"""The Hugging Face dataset card, with every count computed from the tables being uploaded.

The card used to be uploaded by hand once (2026-11-08) and never touched by the weekly refresh, so its
counts and "through" date fell behind the data after the first refresh.
"""
import pandas as pd

START = "2025-01-20"


def render(meetings: pd.DataFrame, attendees: pd.DataFrame, docs: pd.DataFrame, as_of: str) -> str:
    n_m = len(meetings)
    n_a = len(attendees)
    no_att = int((~meetings["meeting_id"].isin(set(attendees["meeting_id"]))).sum())
    n_d = len(docs)
    dup_counts = docs.groupby("sha256").size()
    n_dup = int((dup_counts[dup_counts > 1] - 1).sum())
    n_text = int((docs["text_path"].fillna("") != "").sum())
    n_no_text = n_d - n_text
    return f"""---
license: cc0-1.0
pretty_name: OIRA EO 12866 meetings and handouts
---

# OIRA EO 12866 meetings and handouts

Meetings the Office of Information and Regulatory Affairs held under Executive Order 12866, from https://www.reginfo.gov, with the attendees and the handouts attached to each meeting page. Not affiliated with OMB, OIRA, GSA or reginfo.gov.

Covers meetings dated {START} onward, last read on {as_of}. A weekly job re-reads the previous month and the current month, because meetings can be rescheduled and documents added later; older months are not re-read.

- `data/meetings.parquet`: {n_m:,} meetings, one row each (RIN, agency, rule title, stage, date, requestor and client, counts, link).
- `data/attendees.parquet`: {n_a:,} attendee rows. Some meetings list none ({no_att:,}).
- `data/documents.parquet`: {n_d:,} handout listings with size, SHA-256, page count, and paths to the file and to extracted text. {n_dup:,} listings are byte-identical copies of another handout and are kept under each meeting.
- `handouts/<month>/<document_id>.<ext>`: the files. `text/<month>/<document_id>.txt`: extracted text for {n_text:,} of them.

The first collection (2025-01-20 through 2026-11-08) was checked two ways for each of its 23 months: the site's "Number of records found" against the distinct meeting IDs collected, and again by re-running each month as 7-day ranges. They agreed in every month. October and November 2025 have no meetings on the site. Each weekly refresh checks every month it re-reads against the site's "Number of records found" and uploads nothing if they differ.

Text extraction: {n_no_text:,} handouts have no extracted text (mostly scanned PDFs and images); no OCR was run. Two documents (1118292, 1118293) come back from the site as zero bytes. One PDF (1396392) appears truncated at the source.

Code and checks: https://github.com/abigailhaddad/oira-meetings
"""
