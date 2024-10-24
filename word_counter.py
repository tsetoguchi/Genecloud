import os
from collections import Counter


def count_word_frequencies(directory):
    word_counter = Counter()

    # Read each text file in the specified directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read().lower()  # Read and convert to lowercase
                words = text.split()  # Split the text into words
                word_counter.update(words)  # Update the counter with words

    return word_counter


def print_frequencies(word_counter):
    # Print the word frequencies from highest to lowest
    for word, freq in word_counter.most_common():
        print(f"{word}: {freq}")


def word_count(directory):
    word_frequencies = count_word_frequencies(directory)
    print(word_frequencies)
    return word_frequencies


if __name__ == "__main__":
    # Specify the directory containing text files
    directory = './lyrics'  # Change this to your directory path
    word_count(directory)
