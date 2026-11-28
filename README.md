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

You need Python 3.10 or newer (this project was built and tested on
Python 3.14) and Git.

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

## Assumptions

- Scripts are run from the project root, because file paths like
  `data/support_tickets.json` are relative.
- HTML tags are replaced with a space (not removed) so neighbouring words
  do not join together.
- The first ticket's query contains a `<br>` tag, which is used to test the
  HTML-removal step.
- The stop-word list is the small example list from the assignment.
- Stemming is a basic suffix rule (removes a trailing "s"), so it is not
  perfect. For example, "status" becomes "statu".
- Only the first 5 posts from the API are used.
- The fallback documents use the same fields as real documents, so
  downstream code does not need a special case.

## Challenges and What I Learned

- **Virtual environment committed by mistake:** my first commit included the
  `venv` folder because `.gitignore` did not exist yet. I fixed it by
  restarting the Git history before pushing, and now create `.gitignore`
  before the first `git add`.
- **GitHub email privacy error (GH007):** my first push was rejected because
  my commit used a private email address. I fixed it by using GitHub's
  noreply email in my Git configuration.
- **Simple stemming has limits:** my first stemmer had several suffix rules
  that could cut real words wrongly (for example, "speed" would become
  "spe"). I spotted this while reviewing and simplified it to one plural
  rule that I can explain and defend.
- **Handling failures:** a 200 response can still contain bad data, so I
  catch invalid JSON and missing fields as well as timeouts, connection
  errors and HTTP errors.
- **Testing error handling:** I tested the fallback with a broken URL, a
  404 URL, and a page that is not JSON.
- **A test URL left in the main block:** while testing the fallback I changed
  the script to call a broken URL and nearly committed it. This would have
  made the script always return mock data. I now put the real call back and
  re-run the script before every commit.
- **Choosing what to catch:** `requests` does not raise an error for a 404 by
  default, so I added `raise_for_status()` to turn bad status codes into
  exceptions I could handle.