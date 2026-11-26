import json
import re
from collections import Counter

def load_tickets(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def clean_tickets(tickets):
    seen_ids = set()
    cleaned = []

    for ticket in tickets:
        # Rule 1: skip duplicate ticket_ids
        if ticket["ticket_id"] in seen_ids:
            continue
        seen_ids.add(ticket["ticket_id"])

        # Rule 2: skip invalid queries
        query = ticket["query"]
        if query is None or query.strip() == "":
            continue

        # Rule 3: remove HTML tags, then strip spaces
        query = re.sub(r"<[^>]+>", " ", query)
        query = query.strip()

        cleaned.append({**ticket, "query": query})

    return cleaned

STOP_WORDS = {
    "the", "is", "on", "and", "do", "i", "my", "to",
    "from", "or", "can", "how", "what", "after",
}

def simple_stem(word):
    # only strip a suffix if enough letters remain afterwards
    if word.endswith("ing") and len(word) > 5:
        return word[:-3]
    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"
    if word.endswith("ed") and len(word) > 4:
        return word[:-2]
    if word.endswith("s") and not word.endswith("ss") and len(word) > 3:
        return word[:-1]
    return word

def preprocess_text(text):
    # 1. lowercase
    text = text.lower()

    # 2. remove punctuation: keep only letters, numbers and spaces
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # 3. tokenize: split on whitespace
    tokens = text.split()

    # 4. remove stop words
    tokens = [word for word in tokens if word not in STOP_WORDS]

    # 5.  stemming each word
    tokens = [simple_stem(word) for word in tokens]

    return tokens

def analyze_tickets(cleaned_tickets):
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
    # Step 1: load
    tickets = load_tickets("data/support_tickets.json")
    print("Raw tickets:", len(tickets))

    # Step 2: clean
    cleaned = clean_tickets(tickets)
    print("After cleaning:", len(cleaned))
    print("First cleaned query:", cleaned[0]["query"])

    # Step 3: preprocess each ticket
    print("\nTokens per ticket:")
    for ticket in cleaned:
        print(" ", ticket["ticket_id"], preprocess_text(ticket["query"]))

    # Step 4: analyze (prints counts and top 5, saves JSON)
    print("\nAnalysis:")
    analyze_tickets(cleaned)
    
    