import datetime, os, sys
import pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import refresh


def test_window_midmonth_and_january():
    assert refresh.window(datetime.date(2026, 11, 9)) == [("2026-10", "10/01/2026", "10/31/2026"), ("2026-11", "11/01/2026", "11/09/2026")]
    assert refresh.window(datetime.date(2027, 1, 3))[0] == ("2026-12", "12/01/2026", "12/31/2026")


def test_merge_keeps_old_and_new_wins():
    old = pd.DataFrame({"meeting_id": ["1", "2"], "meeting_type": ["Scheduled", "Completed"]})
    new = pd.DataFrame({"meeting_id": ["1", "3"], "meeting_type": ["Completed", "Scheduled"]})
    m = refresh.merge_by_key(old, new, "meeting_id").set_index("meeting_id")
    assert sorted(m.index) == ["1", "2", "3"] and m.loc["1", "meeting_type"] == "Completed"


def test_attendees_replaced_per_meeting():
    old = pd.DataFrame({"meeting_id": ["1", "1", "2"], "name": ["a", "b", "c"]})
    new = pd.DataFrame({"meeting_id": ["1"], "name": ["z"]})
    a = refresh.merge_attendees(old, new, ["1"])
    assert sorted(a["name"]) == ["c", "z"]


def test_card_counts_come_from_the_tables():
    import card
    m = pd.DataFrame({"meeting_id": ["1", "2", "3"]})
    a = pd.DataFrame({"meeting_id": ["1", "1", "2"]})
    d = pd.DataFrame({"document_id": ["10", "11", "12"], "sha256": ["x", "x", "y"],
                      "text_path": ["text/a.txt", "", None]})
    c = card.render(m, a, d, "2026-11-15")
    assert "3 meetings" in c and "3 attendee rows" in c and "list none (1)" in c
    assert "1 listings are byte-identical" in c and "extracted text for 1 of them" in c
    assert "2 handouts have no extracted text" in c and "last read on 2026-11-15" in c
