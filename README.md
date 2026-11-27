# helpdesk-ai-pipelines

A small Python project that cleans noisy helpdesk tickets, applies basic NLP
preprocessing, and fetches documents from a public API with error handling.

Built as the AI Intern take-home assignment.

## Project Structure

```
helpdesk-ai-pipelines/
├── data/
│   ├── support_tickets.json    # input: raw helpdesk tickets
│   └── cleaned_tickets.json    # output: created by task1
├── task1_nlp_cleaner.py        # Part 1: data cleaning and basic NLP
├── task2_api_client.py         # Part 2: API client with error handling
├── ANSWERS.md                  # Part 3: written answers
├── requirements.txt            # Python packages used
└── README.md
```

## Setup

You need Python 3.8 or newer and Git.

**1. Clone the repository**

```bash
git clone https://github.com/vkaashkrsah/helpdesk-ai-pipelines.git
cd helpdesk-ai-pipelines
```

**2. Create a virtual environment**

Mac / Linux:

```bash
python3 -m venv myvenv
source myvenv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv myvenv
myvenv\Scripts\Activate.ps1
```

When it is active, `(myvenv)` appears at the start of your terminal line.

**3. Install the packages**

```bash
pip install -r requirements.txt
```

## How to Run

Run both scripts from the project root folder, with `(myvenv)` active.

### Part 1: Data cleaning and NLP

```bash
python task1_nlp_cleaner.py
```

This loads `data/support_tickets.json`, cleans it, and prints the results.
It also saves the cleaned and tokenized tickets to `data/cleaned_tickets.json`.

Expected output:

```
Tickets per category: {'IT': 3, 'HR': 2, 'Finance': 1}
Top 5 keywords:
  vpn: 2
  day: 2
  reset: 1
  password: 1
  urgent: 1
```

9 raw tickets become 6 valid ones: 1 duplicate (T-101) and 2 invalid
queries (T-104 whitespace, T-106 null) are removed. Keywords with the same
count appear in the order they were first seen.

### Part 2: API client

```bash
python task2_api_client.py
```

This fetches the first 5 posts from `https://jsonplaceholder.typicode.com/posts`,
reshapes them into documents, and prints them. Logs show when the request
starts and succeeds.

To test the fallback, turn off your Wi-Fi and run the script again. You
should see a `WARNING` log and 2 mock documents, and the program does not crash.