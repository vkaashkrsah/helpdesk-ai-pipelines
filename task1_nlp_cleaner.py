import json  # read and write JSON files
import re  # regular expressions for pattern-based text cleaning
from collections import Counter  # a dictionary that counts items

# Common words that carry little meaning; a set gives fast "in" checks
STOP_WORDS = {
    "the", "is", "on", "and", "do", "i", "my", "to",
    "from", "or", "can", "how", "what", "after",
}


def load_tickets(path):
    # "with" closes the file automatically, even if an error happens
    with open(path, "r", encoding="utf-8") as f:
        # json.load turns JSON text into a Python list of dictionaries
        return json.load(f)


def clean_tickets(tickets):
    seen_ids = set()  # remembers ticket_ids we already kept
    cleaned = []  # the new list of valid tickets

    for ticket in tickets:
        # Rule 1: skip duplicate ticket_ids (the first one is kept)
        if ticket["ticket_id"] in seen_ids:
            continue
        seen_ids.add(ticket["ticket_id"])

        # Rule 2: skip invalid queries (None, empty, or only spaces)
        query = ticket["query"]
        # check None first, because None.strip() would crash
        if query is None or query.strip() == "":
            continue

        # Rule 3: remove HTML tags, then strip spaces
        # replace each tag with a space so neighbouring words don't join
        query = re.sub(r"<[^>]+>", " ", query)
        query = query.strip()

        # copy the ticket with the cleaned query; the original data stays unchanged
        cleaned.append({**ticket, "query": query})

    return cleaned


def simple_stem(word):
    """Basic stemming: turn plurals like 'days' into 'day'."""
    # skip "ss" words (access) and short words (bus) to avoid wrong results
    if word.endswith("s") and not word.endswith("ss") and len(word) > 3:
        return word[:-1]  # cut the last letter
    return word


def preprocess_text(text):
    # 1. lowercase so "VPN" and "vpn" count as the same word
    text = text.lower()

    # 2. remove punctuation: keep only letters, numbers and spaces
    # [^...] means "not these", and a space replaces them so "wi-fi" becomes "wi fi"
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # 3. tokenize: split() with no argument splits on any whitespace
    tokens = text.split()

    # 4. remove stop words (list comprehension: keep a word unless it is a stop word)
    tokens = [word for word in tokens if word not in STOP_WORDS]

    # 5. stemming each word so "day" and "days" are counted together
    tokens = [simple_stem(word) for word in tokens]

    return tokens


def analyze_tickets(cleaned_tickets):
    category_counts = Counter()  # counts tickets per category
    keyword_counts = Counter()  # counts every keyword across all tickets
    records = []  # cleaned tickets plus their tokens, saved to JSON later

    for ticket in cleaned_tickets:
        tokens = preprocess_text(ticket["query"])

        # a Counter starts missing keys at 0, so += 1 works the first time too
        category_counts[ticket["category"]] += 1
        # update() adds every token in the list to the running count
        keyword_counts.update(tokens)

        # copy the ticket and add a new "tokens" field
        records.append({**ticket, "tokens": tokens})

    print("Tickets per category:", dict(category_counts))
    print("Top 5 keywords:")
    # most_common(5) returns the 5 highest counts as (word, count) pairs
    for word, count in keyword_counts.most_common(5):
        print(f"  {word}: {count}")

    # "w" opens the file for writing; indent=2 makes the JSON readable
    with open("data/cleaned_tickets.json", "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    return records


# this block runs only when the file is run directly, not when it is imported
if __name__ == "__main__":
    tickets = load_tickets("data/support_tickets.json")  # step 1: load raw data
    cleaned = clean_tickets(tickets)  # step 2: clean it
    analyze_tickets(cleaned)  # step 3: count, print top keywords, save JSON