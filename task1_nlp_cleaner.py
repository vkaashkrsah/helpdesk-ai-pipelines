import json

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

        cleaned.append(ticket)

    return cleaned

if __name__ == "__main__":
    tickets = load_tickets("data/support_tickets.json")
    print("Raw:", len(tickets))
    cleaned = clean_tickets(tickets)
    print("After cleaning:", len(cleaned))