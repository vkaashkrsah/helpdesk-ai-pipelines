import logging
import requests

API_URL = "https://jsonplaceholder.typicode.com/posts"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

def transform_post(post):
    return {
        "doc_id": post["id"],
        "title": post["title"].strip(),
        "content": post["body"].replace("\n", " ").strip(),
        "word_count": len(post["body"].split()),
    }

def fetch_documents(url=API_URL):
    logger.info("Starting request to %s", url)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        posts = response.json()
        documents = [transform_post(post) for post in posts[:5]]

    except requests.exceptions.Timeout:
        logger.error("Request timed out after 10 seconds.")
        return []

    except requests.exceptions.ConnectionError:
        logger.error("Connection error (offline or bad URL).")
        return []

    except requests.exceptions.HTTPError as err:
        logger.error("HTTP error: %s", err)
        return []

    logger.info("Request succeeded. Fetched %d documents.", len(documents))
    return documents

if __name__ == "__main__":
    docs = fetch_documents()
    for doc in docs:
        print(doc)