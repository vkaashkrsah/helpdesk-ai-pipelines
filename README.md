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