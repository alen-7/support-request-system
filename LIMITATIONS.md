# Limitations and possible improvements

## Limitations
- **No saving.** All data lives in memory. When the program closes, new
  requests, replies and changes are lost. Only the sample file is reloaded.
- **Urgent requests are not served first.** The queue is strictly first in,
  first out, as the task required. "High priority" is a label used for
  sorting; it does not move a request to the front of the queue.
- **Processing cannot be undone.** Undo covers marking urgent, changing the
  status and adding replies. Processing takes a request out of the queue,
  and undo does not put it back.
- **Undo copies a whole request.** Each update stores a full copy, which
  uses more memory for requests with long reply threads.
- **Name search is simple.** It matches part of a name, ignoring case, but
  does not handle typos or similar-sounding names.
- **No real users.** Anyone can change any request; there is no login.
- **Terminal only.** The menu is text-based.

## Possible improvements
- Save and load requests with a JSON file or a database (like the SQL work in B3).
- Use a priority queue (`heapq`) so urgent requests are processed first.
- Store only the changed fields for undo instead of a full copy.
- Add a web API with FastAPI (a later module).
- Add fuzzy name search and a way to export reports.
