import os
import Levenshtein as lev

class TrieNode:
    def __init__(self):
        self.children = {}
        self.sentences = []


class TextTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, file_path, sentence, words):
        node = self.root
        for word in words:
            if word not in node.children:
                node.children[word] = TrieNode()
            node = node.children[word]
            node.sentences.append((file_path, sentence))

    def search(self, query):
        results = []
        node = self.root
        words = query.split()

        for word in words:
            if word not in node.children:
                return results
            node = node.children[word]

        stack = [node]
        while stack:
            current_node = stack.pop()
            results.extend(current_node.sentences)
            stack.extend(current_node.children.values())
        results = list(set(results))
        return results


def search_autocomplete(trie, query):
    results = trie.search(query)

    def calculate_score(text):
        return len(text) * 2  # Basic score calculation

    # Calculate Levenshtein distance and adjust the score
    for i, (file_path, sentence) in enumerate(results):
        lev_distance = lev.distance(query, sentence)
        score = calculate_score(sentence) - lev_distance  # Adjust the score
        results[i] = (file_path, sentence, score)

    results.sort(key=lambda x: x[2], reverse=True)  # Sort by score in descending order

    return results[:5]  # Return the top 5 results


# Main function to build the trie
def build_trie(files_directory):
    if not os.path.exists(files_directory):
        print("Directory does not exist.")
        return None

    trie = TextTrie()
    for root, dirs, files in os.walk(files_directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        trie.insert(file_path, line, line.split())
    return trie


def main():
    files_directory = r'data'

    # Check if the directory exists
    if not os.path.exists(files_directory):
        print("Directory does not exist. Please provide a valid directory path.")
    else:
        trie = build_trie(files_directory)

        while True:
            user_input = input("Enter a sentence/word: ")
            if user_input.lower() == 'exit':
                break
            results = search_autocomplete(trie, user_input)
            for file_path, sentence, score in results:
                print(f"File: {file_path}\nLine: {sentence}\nScore: {score}\n\n")


if __name__ == '__main__':
    main()