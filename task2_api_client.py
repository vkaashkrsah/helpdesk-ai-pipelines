import logging
import requests

API_URL = "https://jsonplaceholder.typicode.com/posts"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

FALLBACK_DOCUMENTS = [
    {
        "doc_id": 0,
        "title": "Fallback document one",
        "content": "This is mock content used when the API is unavailable.",
        "word_count": 10,
    },
    {
        "doc_id": -1,
        "title": "Fallback document two",
        "content": "More mock content so downstream code still has data.",
        "word_count": 9,
    },
]

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
        logger.warning("Request timed out after 10 seconds. Using fallback documents.")
        return list(FALLBACK_DOCUMENTS)

    except requests.exceptions.ConnectionError:
        logger.warning("Connection error (offline or bad URL). Using fallback documents.")
        return list(FALLBACK_DOCUMENTS)

    except requests.exceptions.HTTPError as err:
        logger.warning("HTTP error: %s. Using fallback documents.", err)
        return list(FALLBACK_DOCUMENTS)

    logger.info("Request succeeded. Fetched %d documents.", len(documents))
    return documents

if __name__ == "__main__":
    docs = fetch_documents("https://jsonplaceholder.typicode.invalid/posts")
    for doc in docs:
        print(doc)