# coding: utf-8

import os
from typing import List
from Levenshtein import editops
from trie import Trie, TrieNode
from AutoCompleteData import AutoCompleteData

# Consts
DATA_SUB_DIR = 'data'
TXT_EXTENSION = '.txt'
REPLACE_SCORE = [5, 4, 3, 2, 1]
INSERT_DELETE_SCORE = [10, 8, 6, 4, 2]
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
                            cleaned_word = ''.join([char.lower() if char.isalpha() else char for char in word if
                                                    char.isalpha() or char == ' '])
                            trie.insert(cleaned_word, {
                                "line_number": line_num,
                                "file_name": file.split(".")[0],
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


def search_trie(trie, sentence):
    words = sentence.lower().split()
    mismatched = False
    start_index = 1
    first_word_matches = trie.search(words[0])

    # if not found any word as first input word, mark as first word mismatched and continue with second word
    if not first_word_matches:
        first_word_matches = trie.search(words[1])
        mismatched = True
        start_index = 2

    guessed_sentences = [match for match in first_word_matches if
                         check_sequence_match(trie, match, words, mismatched, start_index)]

    return guessed_sentences, mismatched, words, start_index


def print_completions(completions):
    if completions:
        print("\nPotential completions:")
        for completion in completions:
            print(completion.completed_sentence)
    else:
        print("\nNo matches found for your input.")


def get_offset(line_content, word_index, words, start_index):
    """Compute the offset where the input_sentence starts in line_content."""
    content_words = line_content.lower().split()
    start_word = content_words[word_index]
    return line_content.lower().find(start_word)


def get_score(line_content, input_sentence, offset):

    line_guessed = line_content[offset:offset + len(input_sentence)]

    # Exclude punctuation marks and calculate base score
    base_score = sum(2 for char in input_sentence if char.isalnum())
    score = base_score

    edits = editops(line_guessed, input_sentence)

    for op, _, pos in edits:
        if op == "replace":
            deduction = REPLACE_SCORE[min(pos, 4)]  # We use min to ensure that we never go out of the list bounds
        else:  # for both insert and delete
            deduction = INSERT_DELETE_SCORE[min(pos, 4)]

        score -= deduction

    return score


def get_best_kֵ_completions(trie, user_input) -> List[AutoCompleteData]:
    guessed_sentences, mismatched, input_words, start_index = search_trie(trie, user_input)

    # Create a list to hold potential results
    potential_results = []

    for guess in guessed_sentences:
        offset = get_offset(guess['line_content'], guess['word_index'], input_words, start_index)
        mismatched_word = None if not mismatched else input_words[start_index - 1]
        score = get_score(guess['line_content'], user_input, offset)
        auto_data = AutoCompleteData(guess['line_content'], guess['file_name'], offset, score)
        potential_results.append(auto_data)

    # Sort the potential results by score in descending order
    sorted_results = sorted(potential_results, key=lambda x: x.score, reverse=True)

    return sorted_results


def main():
    print("start")
    data_trie = init(DATA_DIRECTORY)
    print("end read")
    user_input = input("Please enter a sentence for completion: ")

    completions = get_best_kֵ_completions(data_trie, user_input)
    for completion in completions:
        print(completion)


if __name__ == '__main__':
    main()
