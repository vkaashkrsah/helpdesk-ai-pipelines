import json

def load_tickets(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    tickets = load_tickets("data/support_tickets.json")
    print(len(tickets))