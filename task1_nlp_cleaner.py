import json

def load_tickets(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def clean_tickets(tickets):
    seen_ids = set()
    cleaned = []

    for ticket in tickets:
        if ticket["ticket_id"] in seen_ids:
            continue
        seen_ids.add(ticket["ticket_id"])
        cleaned.append(ticket)

    return cleaned

if __name__ == "__main__":
    tickets = load_tickets("data/support_tickets.json")
    print("Raw:", len(tickets))
    cleaned = clean_tickets(tickets)
    print("After removing duplicates:", len(cleaned))