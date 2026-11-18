# Data structure used for each feature

n = number of requests, k = number of replies on one request.

| Feature | Data structure | Why it was chosen | Time | Extra space |
|---------|----------------|-------------------|------|-------------|
| Store a request and customer details | `dict` | Fields have names (customer, status, priority), and a dictionary of requests lets us find one by its ID instantly | O(1) add and look up | O(n) |
| Prevent duplicate request IDs | `set` | A set answers "have I seen this ID?" in constant time and cannot hold duplicates | O(1) check | O(n) |
| Process in the order received | `deque` (queue) | First in, first out. `popleft()` is O(1); a plain list would be O(n) because everything shifts | O(1) add and remove | O(n) |
| Mark urgent / change status | `dict` lookup | Find the request directly, then change one field | O(1) plus the cost of saving an undo copy | O(size of one request) per update |
| Undo the last update | `list` used as a stack | Last in, first out: the newest saved copy is the first one restored | O(1) pop | O(u x size of a request), u = updates stored |
| Search by ID | `dict` lookup (also linear and binary search for comparison) | Fastest option because IDs are the dictionary keys | O(1) average | O(1) |
| Search by customer name | Linear scan | A name can match part of the text, so every request must be checked | O(n) | O(m), m = matches |
| Sort by date, priority or status | `sorted()` (and bubble sort for comparison) | Built-in sort is fast and well tested | O(n log n) | O(n) |
| Show replies and follow-ups in order | Recursion over nested lists | A reply can contain replies, which can contain replies. A function that calls itself matches that shape | O(k) | O(d) call stack, d = depth of the thread |
