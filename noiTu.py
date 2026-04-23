import json
from collections import defaultdict


def build_index(filename):
    index = defaultdict(list)

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                text = data.get("text", "")

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
        print(phrase, end= " , ")
        count = len(next_list)

        if count < min_count:
            # New global minimum found
            min_count = count
            best_words = [phrase]
            best_next_lists = [next_list]

        elif count == min_count:
            # Same minimum → keep all
            best_words.append(phrase)
            best_next_lists.append(next_list)

    return best_words, best_next_lists


def main():
    file_path = "/home/kansu/Desktop/words.txt"
    query = "bóc"
    if query == "":
        query = input("Enter first word: ").strip()

    index = build_index(file_path)
    best_words, next_words = find_best_word(index, query)

    if not best_words:
        print("No matching 2-word phrases found.")
        return
    print("\n=====================================")
    print("\nBest phrases (minimum next options):")
    for i, word in enumerate(best_words):
        print(word)

if __name__ == "__main__":
    main()