import logging
import requests

API_URL = "https://jsonplaceholder.typicode.com/posts"

# Configure logging once: show INFO and above, with a timestamp and level
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Mock documents returned when the API fails; same shape as real documents
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
    # Reshape a raw API post into the document format the assignment asks for
    return {
        "doc_id": post["id"],  # rename "id" to "doc_id"
        "title": post["title"].strip(),
        # replace line breaks with spaces so the content is one line
        "content": post["body"].replace("\n", " ").strip(),
        # split() cuts the text into words, len() counts them
        "word_count": len(post["body"].split()),
    }


def fetch_documents(url=API_URL):
    # the default url means normal use needs no argument, and tests can pass a bad one
    logger.info("Starting request to %s", url)

    # only the risky code goes inside try
    try:
        # timeout stops a stuck server from freezing the program forever
        response = requests.get(url, timeout=10)
        # turns 4xx/5xx status codes (like 404) into an HTTPError we can catch
        response.raise_for_status()
        posts = response.json()
        # posts[:5] slices the first 5 posts; the list comprehension transforms each
        documents = [transform_post(post) for post in posts[:5]]

    except requests.exceptions.Timeout:
        # server took longer than 10 seconds
        logger.warning("Request timed out after 10 seconds. Using fallback documents.")
        # list() returns a copy, so callers can't change the shared fallback list
        return list(FALLBACK_DOCUMENTS)

    except requests.exceptions.ConnectionError:
        # no internet, or the URL is wrong
        logger.warning("Connection error (offline or bad URL). Using fallback documents.")
        return list(FALLBACK_DOCUMENTS)

    except requests.exceptions.HTTPError as err:
        # server replied with an error status such as 404 or 500
        logger.warning("HTTP error: %s. Using fallback documents.", err)
        return list(FALLBACK_DOCUMENTS)

    except (ValueError, KeyError) as err:
        # ValueError: reply is not valid JSON; KeyError: a post is missing a field
        logger.warning("Unexpected response format: %s. Using fallback documents.", err)
        return list(FALLBACK_DOCUMENTS)

    # this line is reached only if nothing failed, because each except returns early
    logger.info("Request succeeded. Fetched %d documents.", len(documents))
    return documents


# runs only when this file is executed directly, not when imported
if __name__ == "__main__":
    docs = fetch_documents()
    for doc in docs:
        print(doc)