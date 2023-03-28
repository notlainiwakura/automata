#This script takes in .txt file and replaces any word preceded by asterisks with dummy data

import re
from random import choice
from string import ascii_letters
import sys
import os


def generate_dummy_word(word_length, is_capitalized):
    dummy_word = ''.join(choice(ascii_letters) for _ in range(word_length))
    if is_capitalized:
        return dummy_word.capitalize()
    else:
        return dummy_word.lower()


def replace_words_with_asterisks(text):
    replaced_words = {}
    words = re.findall(r'\*\w+', text)

    for word in words:
        original_word = word[1:]
        is_capitalized = original_word[0].isupper()

        if original_word not in replaced_words:
            replaced_words[original_word] = generate_dummy_word(len(original_word), is_capitalized)

        text = text.replace(word, replaced_words[original_word])

    return text


def read_input_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def write_output_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = os.path.splitext(input_file)[0] + '_output.txt'

    text = read_input_file(input_file)
    result = replace_words_with_asterisks(text)
    write_output_file(output_file, result)
    print(f"Output written to {output_file}")
