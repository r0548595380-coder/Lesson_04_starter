"""Selection core unit tests (lesson 4)."""
import pytest

import selection_core


@pytest.mark.req("REQ-SEL-01")
def test_valid_selection_is_returned(sample_event):
    selection = selection_core.submit_selection(sample_event, "cli_100", ["med_1"], ["add_to_album"])
    assert selection["media_ids"] == ["med_1"]
    assert selection["service_codes"] == ["add_to_album"]


@pytest.mark.req("REQ-SEL-01")
def test_valid_selection_is_recorded_on_the_event(sample_event):
    selection_core.submit_selection(sample_event, "cli_100", ["med_1", "med_2"], ["add_to_album"])
    assert len(sample_event["selections"]) == 1


@pytest.mark.req("REQ-SEL-01")
def test_empty_media_list_raises_error(sample_event):
    with pytest.raises(selection_core.SelectionError) as exc_info:
        selection_core.submit_selection(sample_event, "cli_100", [], ["add_to_album"])
    assert exc_info.value.code == "SELECTION_EMPTY"


@pytest.mark.req("REQ-SEL-02")
def test_media_not_in_event_raises_error(sample_event):
    with pytest.raises(selection_core.SelectionError) as exc_info:
        selection_core.submit_selection(sample_event, "cli_100", ["med_999"], ["add_to_album"])
    assert exc_info.value.code == "MEDIA_NOT_IN_EVENT"


@pytest.mark.req("REQ-SEL-03")
def test_available_services_lists_enabled_services_only(sample_event):
    assert selection_core.available_services(sample_event) == ["add_to_album"]


@pytest.mark.req("REQ-SEL-03")
def test_disabled_service_raises_error(sample_event):
    with pytest.raises(selection_core.SelectionError) as exc_info:
        selection_core.submit_selection(sample_event, "cli_100", ["med_1"], ["print_10x15"])
    assert exc_info.value.code == "SERVICE_NOT_AVAILABLE"


@pytest.mark.req("REQ-SEL-05")
def test_duplicate_media_raises_error(sample_event):
    with pytest.raises(selection_core.SelectionError) as exc_info:
        selection_core.submit_selection(sample_event, "cli_100", ["med_1", "med_1"], ["add_to_album"])
    assert exc_info.value.code == "DUPLICATE_MEDIA"


@pytest.mark.req("REQ-SEL-06")
def test_wrong_client_raises_forbidden(sample_event):
    with pytest.raises(selection_core.SelectionError) as exc_info:
        selection_core.submit_selection(sample_event, "cli_999", ["med_1"], ["add_to_album"])
    assert exc_info.value.code == "FORBIDDEN"