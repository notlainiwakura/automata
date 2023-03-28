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

def clean_xml(input_file, tags_to_keep):
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Recursively clear text from elements not in the tags_to_keep list
    def clear_unwanted_text(element):
        if element.tag not in tags_to_keep and element.text is not None:
            element.text = None
        for child in element:
            clear_unwanted_text(child)

    clear_unwanted_text(root)

    # Recursively remove empty elements
    def remove_empty_elements(element):
        for child in list(element):
            if not child.text and not child.attrib and len(child) == 0:
                element.remove(child)
            else:
                remove_empty_elements(child)

    remove_empty_elements(root)

    return tree

def write_xml_tree_to_file(tree, output_file):
    # Write the cleaned XML tree to the output file
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

# Set the input and output file paths
input_xml_file = input("Enter the path to the XML file that contains your tests: ")


# List of tags to keep
tags_to_keep = ["title", "preconds", "steps", "expected"]

# Clean the XML file and get the cleaned XML tree
cleaned_tree = clean_xml(input_xml_file, tags_to_keep)


if __name__ == '__main__':
    input_file_directory, input_file_name = os.path.split(input_xml_file)

    # Ask the user if the XML is clean
    is_xml_clean = input("Is the XML file clean? (yes/no): ").lower()

    # If the XML is not clean, run the clean_xml method and its associated methods
    if is_xml_clean != 'yes':
        cleaned_tree = clean_xml(input_xml_file, tags_to_keep)
        output_file_name = f"cleanXML_{input_file_name}"
        output_xml_file = os.path.join(input_file_directory, output_file_name)
        write_xml_tree_to_file(cleaned_tree, output_xml_file)
        input_xml_file = output_xml_file
    else:
        output_file_name = f"pokemoned_{input_file_name}"
        output_xml_file = os.path.join(input_file_directory, output_file_name)
        output_txt_file_name = f"output_{input_file_name.split('.')[0]}.txt"
        output_txt_file = os.path.join(input_file_directory, output_txt_file_name)
        process_xml_file(input_xml_file, output_xml_file, output_txt_file)




