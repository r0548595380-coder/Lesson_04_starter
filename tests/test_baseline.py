"""Tests for baseline tasks (lesson 4)."""
from baseline.tasks import (
    count_selected,
    first_missing,
    group_by_gallery,
    load_events,
    total_price,
)


def test_count_selected_ignores_duplicates():
    assert count_selected(["med_1", "med_2", "med_1"]) == 2
    assert count_selected([]) == 0


def test_group_by_gallery_preserves_order():
    media = [
        {"gallery_id": "gal_1", "id": "med_1"},
        {"gallery_id": "gal_2", "id": "med_3"},
        {"gallery_id": "gal_1", "id": "med_2"},
    ]
    assert group_by_gallery(media) == {
        "gal_1": ["med_1", "med_2"],
        "gal_2": ["med_3"],
    }


def test_total_price_ignores_none():
    assert total_price([1500, None, 2500, None]) == 4000
    assert total_price([None, None]) == 0


def test_first_missing_returns_first_absent_item():
    assert first_missing(["a", "b", "c"], ["a", "c"]) == "b"
    assert first_missing(["a", "b"], ["a", "b"]) is None


def test_load_events_reads_json_file(tmp_path):
    sample = [{"id": "evt_1", "title": "אירוע"}]
    file_path = tmp_path / "events.json"
    file_path.write_text('[{"id": "evt_1", "title": "אירוע"}]', encoding="utf-8")
    assert load_events(file_path) == sample