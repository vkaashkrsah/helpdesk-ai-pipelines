import json
import re
from collections import Counter

STOP_WORDS = {
    "the", "is", "on", "and", "do", "i", "my", "to",
    "from", "or", "can", "how", "what", "after",
}


def load_tickets(path):
    """Load tickets from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def clean_tickets(tickets):
    """Remove duplicate IDs and invalid queries, and strip HTML tags and whitespace."""
    seen_ids = set()
    cleaned = []

    for ticket in tickets:
        if ticket["ticket_id"] in seen_ids:
            continue
        seen_ids.add(ticket["ticket_id"])

        query = ticket["query"]
        # Check for None first: None has no .strip()
        if query is None or query.strip() == "":
            continue

        # Replace tags with a space so neighbouring words do not merge
        query = re.sub(r"<[^>]+>", " ", query).strip()

        # Copy the ticket so the input data is not modified
        cleaned.append({**ticket, "query": query})

    return cleaned


def simple_stem(word):
    """Reduce simple plurals to their singular form (days -> day)."""
    # Skip "ss" words (access) and very short words (bus)
    if word.endswith("s") and not word.endswith("ss") and len(word) > 3:
        return word[:-1]
    return word


def preprocess_text(text):
    """Lowercase, remove punctuation, tokenize, drop stop words and stem."""
    text = text.lower()
    # Replace punctuation with a space so "wi-fi" becomes "wi fi"
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    tokens = text.split()
    tokens = [word for word in tokens if word not in STOP_WORDS]
    return [simple_stem(word) for word in tokens]


def analyze_tickets(cleaned_tickets):
    """Print ticket counts per category and the top 5 keywords, then save the records."""
    category_counts = Counter()
    keyword_counts = Counter()
    records = []

    for ticket in cleaned_tickets:
        tokens = preprocess_text(ticket["query"])
        category_counts[ticket["category"]] += 1
        keyword_counts.update(tokens)
        records.append({**ticket, "tokens": tokens})

    print("Tickets per category:", dict(category_counts))
    print("Top 5 keywords:")
    for word, count in keyword_counts.most_common(5):
        print(f"  {word}: {count}")

    with open("data/cleaned_tickets.json", "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    return records


if __name__ == "__main__":
    tickets = load_tickets("data/support_tickets.json")
    cleaned = clean_tickets(tickets)
    analyze_tickets(cleaned)