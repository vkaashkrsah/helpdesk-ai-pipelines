import json
import re

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

    return cleaned

if __name__ == "__main__":
    tickets = load_tickets("data/support_tickets.json")
    cleaned = clean_tickets(tickets)
    print("After cleaning:", len(cleaned))
    print(cleaned[0]["query"])