import logging

import requests

API_URL = "https://jsonplaceholder.typicode.com/posts"
REQUEST_TIMEOUT = 10  # seconds

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Returned when the API is unavailable; same fields as real documents
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
    """Convert a raw API post into the document format."""
    return {
        "doc_id": post["id"],
        "title": post["title"].strip(),
        "content": post["body"].replace("\n", " ").strip(),
        "word_count": len(post["body"].split()),
    }


def fetch_documents(url=API_URL):
    """Fetch the first 5 posts as documents, or return fallback documents on failure."""
    logger.info("Starting request to %s", url)

    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        # requests does not raise on 4xx/5xx by itself
        response.raise_for_status()
        posts = response.json()
        documents = [transform_post(post) for post in posts[:5]]

    except requests.exceptions.Timeout:
        logger.warning("Request timed out after %d seconds. Using fallback documents.", REQUEST_TIMEOUT)
        return list(FALLBACK_DOCUMENTS)

    except requests.exceptions.ConnectionError:
        logger.warning("Connection error (offline or bad URL). Using fallback documents.")
        return list(FALLBACK_DOCUMENTS)

    except requests.exceptions.HTTPError as err:
        logger.warning("HTTP error: %s. Using fallback documents.", err)
        return list(FALLBACK_DOCUMENTS)

    except (ValueError, KeyError) as err:
        # Invalid JSON, or a post missing an expected field
        logger.warning("Unexpected response format: %s. Using fallback documents.", err)
        return list(FALLBACK_DOCUMENTS)

    logger.info("Request succeeded. Fetched %d documents.", len(documents))
    return documents


if __name__ == "__main__":
    for doc in fetch_documents():
        print(doc)