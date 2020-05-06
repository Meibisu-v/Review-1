import sys
import string
import argparse
import json
from collections import defaultdict
from sys import stdin

alphabet = string.ascii_lowercase
ALPHABET = string.ascii_uppercase
len_alph = len(alphabet)


def get_text(input_file):
    if input_file is None:
        text = sys.stdin.read()
    else:
        with open(input_file, 'r') as file:
            text = file.read()
    return text


def count_frequency(text):
    model = defaultdict(int)
    alpha_count = 0
    for i in text:
        if i.isalpha():
            alpha_count += 1
            model[i.lower()] += 1
    for i in alphabet:
        model[i] /= alpha_count
    return model


def caesar_encryptor(key, text, decode):
    out = list(text)
    for i, char in enumerate(text):
        if char.isalpha():
            if decode:
                t = alphabet.find(char.lower()) - int(key)
                if t < 0:
                    t += len_alph
                letter = alphabet[t % len_alph]
            else:
                letter = alphabet[(alphabet.find(char.lower()) + int(key)) % len_alph]
            out[i] = append_letter(char, letter)
        else:
            out[i] = char
    return ''.join(out)


def vigenere_encryptor(key, text, decode):
    out = []
    new_key = key * (len(text) // len(key) + 1)
    index_key = 0
    for i, char in enumerate(text):
        if char.isalpha():
            if decode:
                t = alphabet.find(char.lower()) - alphabet.find(new_key.lower()[index_key])
                if t < 0:
                    t += len_alph
                letter = alphabet[t % len_alph]
            else:
                letter = alphabet[(alphabet.find(char.lower()) + alphabet.find(new_key.lower()[index_key])) % len_alph]
            out.append(append_letter(char, letter))
            index_key += 1
        else:
            out.append(char)
    return ''.join(out)


def append_letter(char, letter):
    if char.islower():
        return letter
    else:
        return letter.upper()


def print_output(encode_out, output, diagram=False):
    if output is None:
        if diagram:
            print(json.dumps(encode_out))
        else:
            print(encode_out)
    else:
        with open(output, 'w') as file:
            if diagram:
                file.write(json.dumps(encode_out))
            else:
                file.write(encode_out)


def select_function(cipher, inp, key, output, decode=True):
    text = get_text(inp)
    encode_out = ""
    if cipher == 'caesar':
        encode_out = caesar_encryptor(int(key), text, decode is True)
    elif cipher == 'vigenere':
        encode_out = vigenere_encryptor(key, text, decode is True)
    print_output(encode_out, output)


def hack(inp, output, model):
    with open(model, 'r') as model_file:
        model_freq = json.load(model_file)
    text = count_frequency(get_text(inp))
    min_key = -1
    min_dist = 0
    for index in range(len_alph):
        dist = 0
        shift = 0
        for alpha in alphabet:
            dist += (model_freq[alpha] - text[alphabet[(shift - index) % len_alph]]) ** 2
            shift += 1
        if dist < min_dist or min_key == -1:
            min_dist = dist
            min_key = index
    code = caesar_encryptor(min_key, get_inp, False)
    print_output(code, output)
# ---------------------------------------------------


def get_args():
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest='action')
    encode_ = subs.add_parser('encode', help='Encode')
    encode_.add_argument('--cipher', help='Cipher')
    encode_.add_argument('--key', dest='key', help='Key')
    encode_.add_argument('--input-file', required=False, dest='input', help='Input file', default=None)
    encode_.add_argument('--output-file', required=False, dest='output', help='Output file', default=None)
    decode_ = subs.add_parser('decode', help='Decode')
    decode_.add_argument('--cipher', help='Cipher')
    decode_.add_argument('--key', dest='key', help='Key')
    decode_.add_argument('--input-file', required=False, dest='input', help='Input file', default=None)
    decode_.add_argument('--output-file', required=False, dest='output', help='Output file', default=None)
    train_ = subs.add_parser('train', help='Train')
    train_.add_argument('--text-file', required=False,  dest='input', help='Text file', default=None)
    train_.add_argument('--model-file', required=True, dest='model', help='Model file')
    hack_ = subs.add_parser('hack', help='Hack')
    hack_.add_argument('--input-file', required=False, dest='input', help='Input file', default=None)
    hack_.add_argument('--output-file', required=False, dest='output', help='Output file', default=None)
    hack_.add_argument('--model-file', dest='model', help='Model file')
    args = parser.parse_args()
    return args


# -----------------------------------------------------------

# -------------------main------------------------------------


def main():
    args = get_args()
    if args.action == 'encode' or args.action == 'decode':
        select_function(args.cipher, args.input, args.key, args.output, args.action == 'decode')
    if args.action == 'train':
        print_output(count_frequency(get_text(args.input)), args.model, True)
    if args.action == 'hack':
        hack(args.input, args.output, args.model)


if __name__ == '__main__':
    main()
