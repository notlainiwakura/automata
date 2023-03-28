import re
import random
import xml.etree.ElementTree as ET
import os

# A list of Pokemon names to be used to mask sensitive information
pokemon_names = [
    "Pikachu", "Charmander", "Bulbasaur", "Squirtle", "Jigglypuff", "Meowth", "Psyduck", "Snorlax", "Lucario", "Greninja",
    "Eevee", "Vaporeon", "Jolteon", "Flareon", "Mewtwo", "Mew", "Lugia", "Ho-Oh", "Celebi", "Blaziken",
    "Gardevoir", "Swampert", "Torchic", "Mudkip", "Treecko", "Aggron", "Flygon", "Salamence", "Metagross", "Latias"
]


def replace_with_pokemon(match):
    return random.choice(pokemon_names)


def replace_words_with_pokemon(text):
    pattern = r'\*\w+'
    result = re.sub(pattern, replace_with_pokemon, text)
    return result


def process_element(element):
    if element.text:
        element.text = replace_words_with_pokemon(element.text)
    if element.tail:
        element.tail = replace_words_with_pokemon(element.tail)

    for child in element:
        process_element(child)


def write_to_txt_file(title, preconds, steps, expected, output_txt_file):
    with open(output_txt_file, 'a') as txt_file:
        txt_file.write(f"Title: {title}\n")
        txt_file.write(f"Preconditions: {preconds}\n")
        txt_file.write("Steps:\n")

        for step in steps:
            txt_file.write(f"{step}\n")

        txt_file.write(f"Expected Results: {expected}\n\n")

def process_xml_file(input_filename, output_filename, output_txt_file):
    tree = ET.parse(input_filename)
    root = tree.getroot()

    process_element(root)
    tree.write(output_filename)

    for case in root.findall('.//case'):
        title = case.find('title').text
        preconds = case.find('./custom/preconds').text
        steps = [step.strip() for step in case.find('./custom/steps').text.split('\n')]
        expected = case.find('./custom/expected').text
        write_to_txt_file(title, preconds, steps, expected, output_txt_file)


input_xml_file = input("Enter the path to the XML file that contains your tests: ")

if __name__ == '__main__':
    input_file_directory, input_file_name = os.path.split(input_xml_file)
    output_file_name = f"masked_{input_file_name}"
    output_xml_file = os.path.join(input_file_directory, output_file_name)

    output_txt_file_name = f"output_{input_file_name.split('.')[0]}.txt"
    output_txt_file = os.path.join(input_file_directory, output_txt_file_name)

    process_xml_file(input_xml_file, output_xml_file, output_txt_file)



