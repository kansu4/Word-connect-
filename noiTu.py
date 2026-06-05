import json
import time
from collections import defaultdict
import urllib.request
import urllib.parse
import ssl


def build_index(filename):
    index = defaultdict(list)

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                text = data.get("text", "")

                text = text.lower()  # Normalize to lowercase

                # Skip hyphenated words
                if "-" in text:
                    continue

                words = text.split()

                # Only keep 2-word phrases
                if len(words) == 2:
                    index[words[0]].append(text)

            except json.JSONDecodeError:
                continue

    return index


def find_best_word(index, query):
    list1 = index.get(query, [])

    if not list1:
        return [], []

    best_words = []
    best_next_lists = []
    min_count = float("inf")

    for phrase in list1:
        second_word = phrase.split()[1]
        next_list = index.get(second_word, [])
        print(phrase, end=" , ")
        count = len(next_list)

        if count < min_count:
            # New global minimum found
            min_count = count
            best_words = [phrase]
            best_next_lists = [next_list]

        elif count == min_count:
            # Same minimum -> keep all
            best_words.append(phrase)
            best_next_lists.append(next_list)

    return best_words, best_next_lists


def fetch_wiki_search(query_word, results_list, request_timeout=1):
    """Fetch search results from Wiktionary legacy API. Appends to shared results_list."""
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    search_url = f"https://vi.wiktionary.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query_word + ' ')}&srnamespace=0&srlimit=50&format=json&origin=*"

    try:
        req = urllib.request.Request(search_url)
        # Required: Wiktionary blocks requests without a valid User Agent
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')
        # Set socket timeout to request_timeout so it fails fast
        resp = urllib.request.urlopen(req, timeout=request_timeout, context=ssl_ctx)
        data = json.loads(resp.read().decode('utf-8'))

        if 'query' in data and 'search' in data['query']:
            for item in data['query']['search']:
                title = item.get('title', '')
                words = title.lower().split()
                # Only keep 2-word phrases starting with query_word
                if len(words) == 2 and words[0] == query_word.lower():
                    results_list.append(title)
    except Exception:
        pass


def search_wikipedia_phrases(query_word, timeout=1):
    """Search Wiktionary for 2-word phrases with a timeout, returning partial results.
    Uses retries to handle flaky 1 second socket timeouts."""
    start_time = time.time()
    partial_results = []

    while time.time() - start_time < timeout:
        remaining = timeout - (time.time() - start_time)
        if remaining <= 0.1:
            break

        fetch_wiki_search(query_word, partial_results, request_timeout=min(remaining, 2))

        if partial_results:
            break  # Got results, stop retrying

    return partial_results


def main():
    file_path = "words.txt"
    query = "khiết"
    if query == "":
        query = input("Enter first word: ").strip()

    index = build_index(file_path)
    best_words, next_words = find_best_word(index, query)

    if not best_words:
        print("No matching 2-word phrases found.")
        print(f"\nSearching Wiktionary for '{query}'...")
        wiki_results = search_wikipedia_phrases(query, timeout=2)

        if wiki_results:
            print(f"Found {len(wiki_results)} phrases from Wiktionary:")
            for phrase in wiki_results:
                print(f"  {phrase}")
        else:
            print("No results from Wiktionary either.")
        return

    print("\n=====================================")
    print("\nBest phrases (minimum next options):")
    for i, word in enumerate(best_words):
        print(word)


if __name__ == "__main__":
    main()
