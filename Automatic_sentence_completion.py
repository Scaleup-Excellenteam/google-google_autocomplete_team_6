# coding: utf-8

import os

from trie import Trie, TrieNode
from AutoCompleteData import AutoCompleteData

# Consts
DATA_SUB_DIR = 'data'
TXT_EXTENSION = '.txt'
MAX_SCORE = 5
SWAP_CHAR_SCORE = 1
ADD_REMOVE_CHAR_SCORE = 2

# Define the path relative to the current script's directory.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIRECTORY = os.path.join(BASE_DIR, DATA_SUB_DIR)


def init(data_directory):
    trie = Trie()

    for root, _, files in os.walk(data_directory):
        for file in files:
            if file.endswith(TXT_EXTENSION):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 0):
                        cleaned_line = line.strip()
                        words = cleaned_line.split()
                        for word_index, word in enumerate(words):
                            cleaned_word = ''.join([char.lower() if char.isalpha() else char for char in word if char.isalpha() or char == ' '])
                            trie.insert(cleaned_word, {
                                "line_number": line_num,
                                "file_name": file,
                                "line_content": cleaned_line,
                                "word_index": word_index
                            })

    return trie


def check_next_word_match(trie, current_match, word, word_index, mismatched):
    next_word_matches = trie.search(word)

    for next_match in next_word_matches:
        if (
                next_match["file_name"] == current_match["file_name"]
                and next_match["line_number"] == current_match["line_number"]
                and (next_match["word_index"] == word_index or (
                not mismatched and next_match["word_index"] == word_index + 1))
        ):
            return True, mismatched

    if not mismatched:
        return True, True  # Mark mismatched as True
    return False, mismatched  # No sequence match found


def check_sequence_match(trie, current_match, words, mismatched, start_index):
    word_index = current_match["word_index"]

    for i, word in enumerate(words[start_index:], start_index):  # start from the second word
        word_index += 1
        found_in_sequence, mismatched = check_next_word_match(trie, current_match, word, word_index, mismatched)
        if not found_in_sequence and mismatched:
            return False
        if not found_in_sequence:
            word_index += 1
    return True  # Sequence match found


def search_trie(trie,sentence):
    words = sentence.lower().split()
    mismatched = False
    start_index = 1
    first_word_matches = trie.search(words[0])
    if not first_word_matches:
        first_word_matches = trie.search(words[1])
        mismatched = True
        start_index = 2

    guessed_sentence = [match for match in first_word_matches if check_sequence_match(trie, match, words, mismatched, start_index)]

    return guessed_sentence


def complete_sentence(trie, user_input):
    matches = search_trie(trie, user_input)
    return matches


def print_completions(completions):
    if completions:
        print("\nPotential completions:")
        for completion in completions:
            print(completion.completed_sentence)
    else:
        print("\nNo matches found for your input.")

def compute_score(index, score):
    if index < MAX_SCORE:
        return abs(index - MAX_SCORE) * score
    return 1


def main():
    print("start")
    data_trie = init(DATA_DIRECTORY)
    print("end read")
    user_input = input("Please enter a sentence for completion: ")

    completions = complete_sentence(data_trie, user_input)
    print(completions)
   # print_completions(completions)

if __name__ == '__main__':
    main()
