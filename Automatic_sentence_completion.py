import os
import pandas as pd
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
    df = pd.DataFrame(columns=['line_value', 'line_number', 'file_name'])

    for root, _, files in os.walk(data_directory):
        for file in files:
            if file.endswith(TXT_EXTENSION):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 0):
                        df = df.append({
                            "line_value": line.strip(),
                            "line_number": line_num,
                            "file_name": file
                        }, ignore_index=True)

    return df

def complete_sentence(df, user_input):
    # Search for lines that start with the user input
    matches = df[df['line_value'].str.startswith(user_input)]

    completions = []
    for _, row in matches.iterrows():
        score = compute_score()
        completion_data = AutoCompleteData(
            completed_sentence=row['line_value'],
            source_text=row['file_name'],
            offset=row['line_number'],
            score=score
        )
        completions.append(completion_data)

    return completions

def print_completions(completions):
    if completions:
        print("\nPotential completions:")
        for completion in completions:
            print(completion.completed_sentence)
    else:
        print("\nNo matches found for your input.")

def compute_score(index, score):
    if index < MAX_SCORE:
        return (abs(index-MAX_SCORE)*score)
    return 1


def main():
    data_df = init(DATA_DIRECTORY)

    user_input = input("Please enter a sentence for completion: ")
    completions = complete_sentence(data_df, user_input)

    print_completions(completions)

if __name__ == '__main__':
    main()
