import re
import sys
import argparse


def vigenere_cipher_encrypt(text, key):
    def char_shift(char, shift):
        if 'a' <= char <= 'z':
            offset = ord('a')
            return chr((ord(char) - offset + shift) % 26 + offset)
        elif 'A' <= char <= 'Z':
            offset = ord('A')
            return chr((ord(char) - offset + shift) % 26 + offset)
        else:
            return char

    def encrypt_plaintext(match):
        plaintext = match.group()
        encrypted_text = []
        key_len = len(key)
        for i, char in enumerate(plaintext):
            shift = ord(key[i % key_len]) % 26
            encrypted_text.append(char_shift(char, shift))
        return ''.join(encrypted_text)

    pattern = r'<.*?>|"(?:\\.|[^\\"])*"|\'(?:\\.|[^\\\'])*\'|bounds|children|index|name|rcid|translation|color|extends|loadStatus|[^<>]+'
    encrypted_text = re.sub(pattern, encrypt_plaintext, text)
    return encrypted_text


def vigenere_cipher_decrypt(text, key):
    def char_shift(char, shift):
        if 'a' <= char <= 'z':
            offset = ord('a')
            return chr((ord(char) - offset - shift + 26) % 26 + offset)
        elif 'A' <= char <= 'Z':
            offset = ord('A')
            return chr((ord(char) - offset - shift + 26) % 26 + offset)
        else:
            return char

    def decrypt_ciphertext(match):
        ciphertext = match.group()
        decrypted_text = []
        key_len = len(key)
        for i, char in enumerate(ciphertext):
            shift = ord(key[i % key_len]) % 26
            decrypted_text.append(char_shift(char, shift))
        return ''.join(decrypted_text)

    pattern = r'<.*?>|"(?:\\.|[^\\"])*"|\'(?:\\.|[^\\\'])*\'|bounds|children|index|name|rcid|translation|color|extends|loadStatus|[^<>]+'
    decrypted_text = re.sub(pattern, decrypt_ciphertext, text)
    return decrypted_text


def encrypt_string(key):

    text = input("Enter the text to encrypt: ")
    encrypted_text = vigenere_cipher_encrypt(text, key)
    sys.stdout.write("Encrypted text: \n")
    sys.stdout.write(encrypted_text)
    sys.stdout.write("\n")


def encrypt_html_file(file_path, key):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    encrypted_text = vigenere_cipher_encrypt(text, key)

    encrypted_file_path = file_path[:-5] + "_encrypted.html"
    try:
        with open(encrypted_file_path, 'w', encoding='utf-8') as file:
            file.write(encrypted_text)
    except UnicodeEncodeError as e:
        # Replace problematic character with an underscore
        encrypted_text = encrypted_text.replace('\u25cf', '_')
        with open(encrypted_file_path, 'w', encoding='utf-8') as file:
            file.write(encrypted_text)


def decrypt_string(key):
    text = input("Enter the text to decrypt: ")
    decrypted_text = vigenere_cipher_decrypt(text, key)
    sys.stdout.write("Decrypted text: ")
    sys.stdout.write(decrypted_text)


def decrypt_html_file(file_path, key):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    decrypted_text = vigenere_cipher_decrypt(text, key)
    decrypted_file_path = file_path[:-5] + "_decrypted.html"
    try:
        with open(decrypted_file_path, 'w', encoding='utf-8') as file:
            file.write(decrypted_text)
    except UnicodeEncodeError as e:
        # Replace problematic character with an underscore
        decrypted_text = decrypted_text.replace('\u25cf', '_')
        with open(decrypted_file_path, 'w', encoding='utf-8') as file:
            file.write(decrypted_text)


def main():
    parser = argparse.ArgumentParser(description='Vigenere cipher encryption/decryption')
    parser.add_argument('-f', '--file', help='path to HTML file')
    parser.add_argument('-k', '--key', help='encryption/decryption key')
    parser.add_argument('-m', '--mode', help='E for encryption or D for decryption')
    parser.add_argument('-t', '--text', help='text to encrypt/decrypt')
    args = parser.parse_args()

    if args.file and args.mode and args.key:
        if args.mode == 'E':
            encrypt_html_file(args.file, args.key)
            sys.stdout.write("Encryption complete!")
        elif args.mode == 'D':
            decrypt_html_file(args.file, args.key)
            sys.stdout.write("Decryption complete!")
        else:
            sys.stdout.write("Invalid mode entered. Please enter 'E' to encrypt or 'D' to decrypt.")

    elif args.text and args.mode and args.key:
        if args.mode == 'E':
            encrypted_text = vigenere_cipher_encrypt(args.text, args.key)
            sys.stdout.write("Encrypted text: ")
            sys.stdout.write(encrypted_text)
        elif args.mode == 'D':
            decrypted_text = vigenere_cipher_decrypt(args.text, args.key)
            sys.stdout.write("Decrypted text: ")
            sys.stdout.write(decrypted_text)
        else:
            sys.stdout.write("Invalid mode entered. Please enter 'E' to encrypt or 'D' to decrypt.")

    else:
        sys.stdout.write("Invalid arguments entered. Please enter either -f, -k, and -m to encrypt/decrypt an HTML file or -t, -k, and -m to encrypt/decrypt a string.")
        
        # Call encrypt_string() or decrypt_string() if no file path is specified
        if args.text and args.mode and args.key:
            if args.mode == 'E':
                sys.stdout.write("Calling encrypt_string() function...")
                encrypt_string(args.key)
            elif args.mode == 'D':
                decrypt_string(args.key)
            else:
                sys.stdout.write("Invalid mode entered. Please enter 'E' to encrypt or 'D' to decrypt.")

if __name__ == "__main__":
    main()