import requests

API_URL = "https://jsonplaceholder.typicode.com/posts"


def transform_post(post):
    return {
        "doc_id": post["id"],
        "title": post["title"].strip(),
        "content": post["body"].replace("\n", " ").strip(),
        "word_count": len(post["body"].split()),
    }


if __name__ == "__main__":
    response = requests.get(API_URL, timeout=10)
    posts = response.json()
    first_five = posts[:5]
    documents = [transform_post(post) for post in first_five]
    print(len(documents))
    for doc in documents:
        print(doc)