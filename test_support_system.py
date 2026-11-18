import pytest

from search_sort import (
    binary_search_by_id,
    bubble_sort,
    builtin_sort,
    linear_search_by_id,
)
from support_system import SupportSystem, count_replies, find_reply, format_thread


def build_system():
    system = SupportSystem()
    system.add_request(
        "REQ-001", "Ada Okafor", "ada@example.com", "Cannot log in", "2026-11-02"
    )
    system.add_request(
        "REQ-002",
        "Bola Adeyemi",
        "bola@example.com",
        "Double charge",
        "2026-11-01",
        urgent=True,
    )
    system.add_request(
        "REQ-003", "Chidi Eze", "chidi@example.com", "Slow app", "2026-11-03"
    )
    return system


# ----- adding requests, dictionaries and the set -----


def test_add_request_stores_customer_in_dictionary():
    system = build_system()
    request = system.search_by_id("REQ-001")
    assert request["customer"] == {"name": "Ada Okafor", "email": "ada@example.com"}
    assert request["status"] == "open"
    assert request["priority"] == "normal"


def test_duplicate_request_id_is_rejected():
    system = build_system()
    with pytest.raises(ValueError):
        system.add_request(
            "REQ-001", "Someone Else", "x@example.com", "Hello", "2026-11-04"
        )
    assert len(system.requests) == 3


def test_empty_message_is_rejected():
    system = SupportSystem()
    with pytest.raises(ValueError):
        system.add_request("REQ-010", "Ada", "ada@example.com", "   ", "2026-11-04")


def test_invalid_date_is_rejected():
    system = SupportSystem()
    with pytest.raises(ValueError):
        system.add_request("REQ-010", "Ada", "ada@example.com", "Hi", "not-a-date")


# ----- queue -----


def test_queue_processes_in_order_received():
    system = build_system()
    assert system.process_next()["request_id"] == "REQ-001"
    assert system.process_next()["request_id"] == "REQ-002"
    assert system.process_next()["request_id"] == "REQ-003"


def test_empty_queue_returns_none():
    assert SupportSystem().process_next() is None


def test_processing_moves_status_to_in_progress():
    system = build_system()
    request = system.process_next()
    assert request["status"] == "in_progress"


# ----- priority and undo (stack) -----


def test_mark_urgent_sets_high_priority():
    system = build_system()
    system.mark_urgent("REQ-001")
    assert system.search_by_id("REQ-001")["priority"] == "high"


def test_undo_restores_previous_version():
    system = build_system()
    system.mark_urgent("REQ-001")
    system.set_status("REQ-001", "closed")
    system.undo()  # undoes the status change only
    request = system.search_by_id("REQ-001")
    assert request["status"] == "open"
    assert request["priority"] == "high"
    system.undo()  # now undoes the urgent marking
    assert system.search_by_id("REQ-001")["priority"] == "normal"


def test_undo_with_nothing_to_undo_returns_none():
    assert SupportSystem().undo() is None


def test_invalid_status_is_rejected():
    system = build_system()
    with pytest.raises(ValueError):
        system.set_status("REQ-001", "finished")


# ----- searching -----


def test_search_by_id_found_and_not_found():
    system = build_system()
    assert system.search_by_id("REQ-002")["customer"]["name"] == "Bola Adeyemi"
    assert system.search_by_id("REQ-999") is None


def test_search_by_customer_name_is_case_insensitive_and_partial():
    system = build_system()
    matches = system.search_by_customer("okaf")
    assert [r["request_id"] for r in matches] == ["REQ-001"]
    assert system.search_by_customer("nobody") == []


# ----- sorting -----


def ids(requests):
    return [r["request_id"] for r in requests]


def test_sort_by_date():
    system = build_system()
    assert ids(system.sort_requests("date")) == ["REQ-002", "REQ-001", "REQ-003"]


def test_sort_by_priority_puts_high_first():
    system = build_system()
    assert ids(system.sort_requests("priority"))[0] == "REQ-002"


def test_sort_by_status():
    system = build_system()
    system.set_status("REQ-003", "closed")
    system.set_status("REQ-001", "in_progress")
    assert ids(system.sort_requests("status")) == ["REQ-002", "REQ-001", "REQ-003"]


@pytest.mark.parametrize("by", ["date", "priority", "status"])
def test_bubble_sort_matches_builtin_sort(by):
    system = build_system()
    assert ids(system.sort_requests(by, "bubble")) == ids(
        system.sort_requests(by, "builtin")
    )


def test_invalid_sort_field_is_rejected():
    with pytest.raises(ValueError):
        build_system().sort_requests("colour")


# ----- search and sort algorithms on their own -----


def test_linear_and_binary_search_agree():
    items = sorted(build_system().requests.values(), key=lambda r: r["request_id"])
    assert linear_search_by_id(items, "REQ-002") == binary_search_by_id(
        items, "REQ-002"
    )
    assert linear_search_by_id(items, "REQ-404") is None
    assert binary_search_by_id(items, "REQ-404") is None


def test_bubble_sort_handles_empty_and_single_item_lists():
    assert bubble_sort([], key=lambda x: x) == []
    assert bubble_sort([5], key=lambda x: x) == [5]
    assert builtin_sort([3, 1, 2], key=lambda x: x) == [1, 2, 3]


# ----- recursion: nested replies -----


def test_nested_replies_are_displayed_in_order_with_indentation():
    system = build_system()
    first = system.add_reply("REQ-001", "Agent", "Try resetting your password")
    second = system.add_reply(
        "REQ-001", "Ada", "No email arrived", reply_to=first["reply_id"]
    )
    system.add_reply("REQ-001", "Agent", "Checking now", reply_to=second["reply_id"])
    lines = format_thread(system.search_by_id("REQ-001")["replies"])
    assert lines == [
        "- [1] Agent: Try resetting your password",
        "  - [2] Ada: No email arrived",
        "    - [3] Agent: Checking now",
    ]


def test_count_and_find_replies_recursively():
    system = build_system()
    first = system.add_reply("REQ-001", "Agent", "Hello")
    system.add_reply("REQ-001", "Ada", "Hi", reply_to=first["reply_id"])
    replies = system.search_by_id("REQ-001")["replies"]
    assert count_replies(replies) == 2
    assert find_reply(replies, 2)["author"] == "Ada"
    assert find_reply(replies, 99) is None


def test_reply_to_missing_reply_is_rejected():
    system = build_system()
    with pytest.raises(ValueError):
        system.add_reply("REQ-001", "Agent", "Hello", reply_to=42)


def test_undo_removes_a_reply():
    system = build_system()
    system.add_reply("REQ-001", "Agent", "Hello")
    system.undo()
    assert system.search_by_id("REQ-001")["replies"] == []


# ----- sample data -----


def test_sample_data_loads():
    system = SupportSystem()
    system.load_from_json("sample_requests.json")
    assert len(system.requests) == 8
    assert count_replies(system.search_by_id("REQ-001")["replies"]) == 3
    assert len(system.queue) == 8
