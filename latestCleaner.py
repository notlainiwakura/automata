import re
import random
import xml.etree.ElementTree as ET
import os

# A list of Pokemon names to be used to mask sensitive information
pokemon_names = [
    "Pikachu", "Charmander", "Bulbasaur", "Squirtle", "Jigglypuff", "Meowth", "Psyduck", "Snorlax", "Lucario", "Greninja",
    "Eevee", "Vaporeon", "Jolteon", "Flareon", "Mewtwo", "Mew", "Lugia", "Ho-Oh", "Celebi", "Blaziken",
    "Gardevoir", "Swampert", "Torchic", "Mudkip", "Treecko", "Aggron", "Flygon", "Salamence", "Metagross", "Latias",
    "Latios", "Kyogre", "Groudon", "Rayquaza", "Jirachi", "Deoxys", "Turtwig", "Chimchar", "Piplup", "Dialga",
    "Palkia", "Heatran", "Giratina", "Cresselia", "Darkrai", "Arceus", "Victini", "Snivy", "Tepig", "Oshawott"
]
# Add a global variable to store the replacements
replacements = {}


def replace_with_pokemon(original_value):
    pokemon = random.choice(pokemon_names)
    replacements[original_value] = pokemon
    return pokemon


def revert_replacements(text):
    modified_text = text
    for original, replacement in replacements.items():
        modified_text = modified_text.replace(replacement, original)
    return modified_text


def replace_words_with_pokemon(text):
    pattern = r'\*\w+'

    def wrapped_replace(match):
        return replace_with_pokemon(match.group(0))

    result = re.sub(pattern, wrapped_replace, text)
    return result


def process_element(element):
    if element.text:
        element.text = replace_words_with_pokemon(element.text)
    if element.tail:
        element.tail = replace_words_with_pokemon(element.tail)

    for child in element:
        process_element(child)


def write_to_txt_file(title, preconds, steps, expected, output_txt_file):
    # Open the file in append mode ('a'), which will create a new file if it does not exist
    with open(output_txt_file, 'a', encoding='utf-8') as txt_file:
        txt_file.write(f"Title: {title}\n")
        txt_file.write(f"Preconditions: {preconds}\n")
        txt_file.write("Steps:\n")

        for step in steps:
            txt_file.write(f"{step}\n")

        txt_file.write(f"Expected Results: {expected}\n\n")


def process_xml_file(input_filename, output_filename, output_txt_file):
    try:
        tree = ET.parse(input_filename)
        root = tree.getroot()

        process_element(root)
        tree.write(output_filename)

        for test in root.findall('.//test'):
            title = test.find('title')
            preconds = test.find('./custom/preconds')
            steps = test.find('./custom/steps')
            expected = test.find('./custom/expected')

            if title is not None and preconds is not None and steps is not None and expected is not None:
                title_text = title.text
                preconds_text = preconds.text
                steps_list = [step.strip() for step in steps.text.split('\n')]
                expected_text = expected.text

                write_to_txt_file(title_text, preconds_text, steps_list, expected_text, output_txt_file)
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
    except Exception as e:
        print(f"Error processing XML file: {e}")


def read_replacements_from_file(replacements_file):
    with open(replacements_file, "r", encoding="utf-8") as f:
        replacements = {}
        for line in f.readlines():
            original, replacement = line.strip().split(" -> ")
            replacements[replacement] = original
        return replacements


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


def write_replacements_to_file(output_directory, replacements):
    replacements_file = os.path.join(output_directory, "replacements.txt")
    with open(replacements_file, "w", encoding="utf-8") as f:
        for original, replacement in replacements.items():
            f.write(f"{original} -> {replacement}\n")


def write_xml_tree_to_file(tree, output_file):
    # Write the cleaned XML tree to the output file
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

# Set the input and output file paths
input_xml_file = input("Enter the path to the XML file that contains your tests: ")


# List of tags to keep
tags_to_keep = ["title", "preconds", "steps", "expected"]

# Clean the XML file and get the cleaned XML tree
cleaned_tree = clean_xml(input_xml_file, tags_to_keep)


def process_text_file(input_filename, output_filename, replacements):
    try:
        with open(input_filename, 'r', encoding='utf-8') as input_file:
            content = input_file.read()

        decrypted_content = revert_replacements(content)

        with open(output_filename, 'w', encoding='utf-8') as output_file:
            output_file.write(decrypted_content)

    except Exception as e:
        print(f"Error processing text file: {e}")


if __name__ == '__main__':

    user_choice = input("Would you like to encrypt your data or decrypt it? Enter E to encrypt, D to decrypt: ").upper()

    if user_choice == "E":

        input_file_directory, input_file_name = os.path.split(input_xml_file)

        # Ask the user if the XML is clean
        is_xml_clean = input("Is the file ready to be pokemoned? (yes/no): ").lower()

        # If the XML is not clean, run the clean_xml method and its associated methods
        if is_xml_clean != 'yes':
            cleaned_tree = clean_xml(input_xml_file, tags_to_keep)
            output_file_name = f"clean_{input_file_name}"
            output_xml_file = os.path.join(input_file_directory, output_file_name)
            write_xml_tree_to_file(cleaned_tree, output_xml_file)
            input_xml_file = output_xml_file
        else:
            output_file_name = f"pokemoned_{input_file_name}"
            output_xml_file = os.path.join(input_file_directory, output_file_name)
            output_txt_file_name = f"output_{input_file_name.split('.')[0]}.txt"

            output_txt_file = os.path.join(input_file_directory, output_txt_file_name)

            # Call the process_xml_file function only when is_xml_clean is 'yes'
            process_xml_file(input_xml_file, output_xml_file, output_txt_file)

            # Remove the output XML file
            os.remove(output_xml_file)

            # Write the replacements to a new text file in the same directory
            write_replacements_to_file(input_file_directory, replacements)

    # Print the replacements
        print("Replacements:")
        for original, replacement in replacements.items():
            print(f"{original} -> {replacement}")

    elif user_choice == "D":

        file_type = input("Enter the type of file you want to decrypt: 'xml' or 'txt': ").lower()

        input_replacements_file = input("Enter the path to the replacements file: ")
        if file_type == "xml":
            replacements = read_replacements_from_file(input_replacements_file)

            input_file_directory, input_file_name = os.path.split(input_xml_file)
            decrypted_file_name = f"decrypted_{input_file_name}"
            output_xml_file = os.path.join(input_file_directory, decrypted_file_name)

            try:
                tree = ET.parse(input_xml_file)
                root = tree.getroot()

                for element in root.iter():
                    if element.text:
                        element.text = revert_replacements(element.text)
                    if element.tail:
                        element.tail = revert_replacements(element.tail)

                tree.write(output_xml_file)

            except ET.ParseError as e:
                print(f"Error parsing XML file: {e}")
            except Exception as e:
                print(f"Error processing XML file: {e}")

        elif file_type == "txt":
            input_text_file = input("Enter the path to the text file that you want to decrypt: ")
            input_file_directory, input_file_name = os.path.split(input_text_file)
            decrypted_file_name = f"decrypted_{input_file_name}"
            output_text_file = os.path.join(input_file_directory, decrypted_file_name)

            process_text_file(input_text_file, output_text_file, replacements)

        else:
            print("Invalid input. Please enter 'xml' or 'txt' for the file type.")
    else:
        print("Invalid input. Please enter E to encrypt or D to decrypt.")

