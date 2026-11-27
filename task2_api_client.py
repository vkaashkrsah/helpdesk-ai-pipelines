import requests

API_URL = "https://jsonplaceholder.typicode.com/posts"

if __name__ == "__main__":
    response = requests.get(API_URL, timeout=10)
    print(response.status_code)
    posts = response.json()
    print(len(posts))
    print(posts[0])