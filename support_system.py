"""Customer support request system (Module B2).

Data structures used (see DATA_STRUCTURES.md for the full table):
  dict   -> each request and the customer's details
  set    -> blocks duplicate request IDs
  deque  -> queue: requests are processed in the order they arrive
  list   -> stack: remembers old versions so the last update can be undone
  recursion -> displays nested replies / follow-up messages
"""

import copy
import json
from collections import deque
from datetime import date
from pathlib import Path

from search_sort import bubble_sort, builtin_sort

BASE_DIR = Path(__file__).parent

PRIORITY_ORDER = {"high": 0, "normal": 1}
STATUS_ORDER = {"open": 0, "in_progress": 1, "closed": 2}


# ---------- Recursion: replies are nested (a reply can have replies) ----------


def count_replies(replies):
    """Count every reply, including replies to replies."""
    total = 0
    for reply in replies:
        total += 1 + count_replies(reply["replies"])  # recursive call
    return total


def format_thread(replies, depth=0):
    """Return the reply thread as indented text lines, in order."""
    lines = []
    for reply in replies:
        indent = "  " * depth
        lines.append(
            f"{indent}- [{reply['reply_id']}] {reply['author']}: {reply['text']}"
        )
        lines.extend(format_thread(reply["replies"], depth + 1))  # recursive call
    return lines


def find_reply(replies, reply_id):
    """Find a reply by its ID anywhere in the thread, or return None."""
    for reply in replies:
        if reply["reply_id"] == reply_id:
            return reply
        found = find_reply(reply["replies"], reply_id)  # recursive call
        if found is not None:
            return found
    return None


# ---------- The main system ----------


class SupportSystem:
    def __init__(self):
        self.requests = {}  # dict: request_id -> request details
        self.used_ids = set()  # set: every ID ever used (no duplicates)
        self.queue = deque()  # queue: IDs waiting to be processed
        self.undo_stack = []  # stack: old versions of updated requests

    # ----- adding and reading -----

    def add_request(
        self, request_id, customer_name, email, message, created=None, urgent=False
    ):
        request_id = request_id.strip()
        if not request_id:
            raise ValueError("Request ID cannot be empty")
        if request_id in self.used_ids:
            raise ValueError(f"Request ID {request_id} already exists")
        if not customer_name.strip():
            raise ValueError("Customer name cannot be empty")
        if not message.strip():
            raise ValueError("Message cannot be empty")
        if created is None:
            created = date.today().isoformat()
        date.fromisoformat(created)  # raises ValueError if the date is invalid

        request = {
            "request_id": request_id,
            "customer": {"name": customer_name.strip(), "email": email.strip()},
            "message": message.strip(),
            "created": created,
            "priority": "high" if urgent else "normal",
            "status": "open",
            "replies": [],
            "next_reply_id": 1,
        }
        self.requests[request_id] = request
        self.used_ids.add(request_id)
        self.queue.append(request_id)
        return request

    def _get(self, request_id):
        request = self.requests.get(request_id.strip())
        if request is None:
            raise ValueError(f"Request {request_id} not found")
        return request

    def _save_for_undo(self, request):
        self.undo_stack.append(copy.deepcopy(request))

    # ----- updates (each one can be undone) -----

    def mark_urgent(self, request_id):
        request = self._get(request_id)
        self._save_for_undo(request)
        request["priority"] = "high"
        return request

    def set_status(self, request_id, status):
        if status not in STATUS_ORDER:
            raise ValueError("Status must be: open, in_progress or closed")
        request = self._get(request_id)
        self._save_for_undo(request)
        request["status"] = status
        return request

    def add_reply(self, request_id, author, text, reply_to=None):
        """Add a reply to the request, or to an existing reply (reply_to)."""
        if not text.strip():
            raise ValueError("Reply text cannot be empty")
        request = self._get(request_id)
        if reply_to is None:
            target = request["replies"]
        else:
            parent = find_reply(request["replies"], reply_to)
            if parent is None:
                raise ValueError(f"Reply {reply_to} not found")
            target = parent["replies"]
        self._save_for_undo(request)
        new_reply = {
            "reply_id": request["next_reply_id"],
            "author": author.strip() or "Unknown",
            "text": text.strip(),
            "replies": [],
        }
        request["next_reply_id"] += 1
        target.append(new_reply)
        return new_reply

    def undo(self):
        """Undo the most recent update. Returns the restored request or None."""
        if not self.undo_stack:
            return None
        old_version = self.undo_stack.pop()
        self.requests[old_version["request_id"]] = old_version
        return old_version

    # ----- queue -----

    def process_next(self):
        """Take the oldest waiting request (first in, first out)."""
        if not self.queue:
            return None
        request = self.requests[self.queue.popleft()]
        if request["status"] == "open":
            request["status"] = "in_progress"
        return request

    # ----- searching -----

    def search_by_id(self, request_id):
        return self.requests.get(request_id.strip())  # dict lookup

    def search_by_customer(self, name):
        """Find every request whose customer name contains the text."""
        name = name.strip().lower()
        matches = []
        for request in self.requests.values():  # linear scan
            if name in request["customer"]["name"].lower():
                matches.append(request)
        return matches

    # ----- sorting -----

    def sort_requests(self, by="date", method="builtin"):
        keys = {
            "date": lambda r: (r["created"], r["request_id"]),
            "priority": lambda r: (
                PRIORITY_ORDER[r["priority"]],
                r["created"],
                r["request_id"],
            ),
            "status": lambda r: (
                STATUS_ORDER[r["status"]],
                r["created"],
                r["request_id"],
            ),
        }
        if by not in keys:
            raise ValueError("Sort by: date, priority or status")
        items = list(self.requests.values())
        if method == "bubble":
            return bubble_sort(items, keys[by])
        return builtin_sort(items, keys[by])

    # ----- loading sample data -----

    def load_from_json(self, path):
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        for item in data:
            request = self.add_request(
                item["request_id"],
                item["customer_name"],
                item["email"],
                item["message"],
                item["created"],
                urgent=item.get("priority") == "high",
            )
            request["status"] = item.get("status", "open")
            request["replies"] = item.get("replies", [])
            request["next_reply_id"] = count_replies(request["replies"]) + 1


# ---------- Simple menu (command line) ----------

MENU = """
==== Support Request System ====
1. Add a request
2. Process next request (queue)
3. Mark a request as urgent
4. Change a request's status
5. Add a reply / follow-up
6. Show a request's reply thread
7. Search (by ID or customer name)
8. Sort and list requests
9. Undo last update
0. Exit
"""


def ask(prompt):
    return input(prompt).strip()


def show_request(request):
    print(
        f"{request['request_id']} | {request['created']} | "
        f"{request['priority']:<6} | {request['status']:<11} | "
        f"{request['customer']['name']} - {request['message']}"
    )


def add_flow(system):
    request = system.add_request(
        ask("Request ID (e.g. REQ-100): "),
        ask("Customer name: "),
        ask("Customer email: "),
        ask("Message: "),
        ask("Date (YYYY-MM-DD, blank for today): ") or None,
        urgent=ask("Urgent? (y/n): ").lower() == "y",
    )
    print("Added:")
    show_request(request)


def reply_flow(system):
    request_id = ask("Request ID: ")
    author = ask("Your name: ")
    text = ask("Reply text: ")
    reply_to = ask("Reply to which reply number? (blank for the main thread): ")
    system.add_reply(request_id, author, text, int(reply_to) if reply_to else None)
    print("Reply added.")


def search_flow(system):
    choice = ask("Search by (1) ID or (2) customer name: ")
    if choice == "1":
        found = system.search_by_id(ask("Request ID: "))
        results = [found] if found else []
    else:
        results = system.search_by_customer(ask("Customer name: "))
    if not results:
        print("No matching requests.")
    for request in results:
        show_request(request)


def sort_flow(system):
    by = ask("Sort by (date / priority / status): ").lower()
    method = ask("Method (builtin / bubble): ").lower() or "builtin"
    for request in system.sort_requests(by, method):
        show_request(request)


def main():
    system = SupportSystem()
    sample = BASE_DIR / "sample_requests.json"
    if sample.exists():
        system.load_from_json(sample)
        print(f"Loaded {len(system.requests)} sample requests.")

    while True:
        print(MENU)
        choice = ask("Choose an option: ")
        try:
            if choice == "1":
                add_flow(system)
            elif choice == "2":
                request = system.process_next()
                if request:
                    print("Now processing:")
                    show_request(request)
                else:
                    print("The queue is empty.")
            elif choice == "3":
                show_request(system.mark_urgent(ask("Request ID: ")))
            elif choice == "4":
                show_request(
                    system.set_status(ask("Request ID: "), ask("New status: "))
                )
            elif choice == "5":
                reply_flow(system)
            elif choice == "6":
                request = system._get(ask("Request ID: "))
                lines = format_thread(request["replies"])
                print("\n".join(lines) if lines else "No replies yet.")
            elif choice == "7":
                search_flow(system)
            elif choice == "8":
                sort_flow(system)
            elif choice == "9":
                restored = system.undo()
                if restored:
                    print("Undid the last update. Restored:")
                    show_request(restored)
                else:
                    print("Nothing to undo.")
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Please choose a number from the menu.")
        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
