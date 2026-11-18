# Support Request System (Module B2)

A Python program that receives, organises and processes customer support
requests. Built for the FlexiSAF Internship Program, AI Engineering pathway,
Module B2: Problem solving, data structures and algorithms.

Author: Chinecherem Ude

## What it does
- Add a new support request
- Store customer information using dictionaries
- Block duplicate request IDs using a set
- Process requests in the order received using a queue
- Mark urgent requests as high priority
- Undo the most recent update using a stack
- Search by request ID or customer name
- Sort by date, priority or status
- Show nested replies and follow-ups in order using recursion
- Compare two searching approaches and two sorting approaches

## Requirements
- Python 3.11 or newer
- Git

## Setup
```bash
git clone https://github.com/alen-7/support-request-system.git
cd support-request-system
python -m venv .venv
```

Activate the environment:
- Windows (Command Prompt): `.venv\Scripts\activate.bat`
- Windows (PowerShell): `.venv\Scripts\Activate.ps1`
- Mac/Linux: `source .venv/bin/activate`

Install the requirements:
```bash
python -m pip install -r requirements.txt
```

## Run the program
```bash
python support_system.py
```
It loads `sample_requests.json` (8 sample requests) and shows a menu.
Try: option 8 (sort), option 7 (search), option 6 and enter `REQ-001`
(nested replies), then option 3 followed by option 9 (undo).

## Run the tests
```bash
python -m pytest
```

## Compare the algorithms
```bash
python compare_algorithms.py
```

## Files
| File | Purpose |
|------|---------|
| `support_system.py` | The main program (SupportSystem class and menu) |
| `search_sort.py` | Linear search, binary search, bubble sort, built-in sort |
| `compare_algorithms.py` | Times the search and sort approaches |
| `sample_requests.json` | Sample support-request data |
| `test_support_system.py` | Automated tests |
| `DATA_STRUCTURES.md` | Which data structure is used for each feature, and why |
| `COMPARISON.md` | Comparison of the searching and sorting approaches |
| `LIMITATIONS.md` | Limitations and possible improvements |
