import sys
import string
import argparse
import json
from collections import defaultdict

alphabet = string.ascii_lowercase
ALPHABET = string.ascii_uppercase
len_alph = len(alphabet)


def get_text(input_file):
    if input_file == sys.stdin:
        text = input()
    else:
        with open(input_file, 'r') as file:
            text = file.read()
    return text


def count_frequency(text):
    model = defaultdict(int)
    alpha_count = 0
    for i in text:
        if i.islower() or i.isupper():
            alpha_count += 1
            model[i.lower()] += 1
    for i in alphabet:
        model[i] /= alpha_count
    return model


def print_diagram(dict_, out):
    if out == sys.stdout:
        print(json.dumps(dict_))
    else:
        with open(out, 'w') as file:
            file.write(json.dumps(dict_))


def caesar_encryptor(key, text, decode):
    out = []
    for i in text:
        if i.isalpha():
            if decode:
                t = alphabet.find(i.lower()) - int(key)
                if t < 0:
                    t += len_alph
                letter = alphabet[t % len_alph]
            else:
                letter = alphabet[(alphabet.find(i.lower()) + int(key)) % len_alph]
            out.append(append_letter(i, letter))
        else:
            out.append(i)
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


def append_letter(i, letter):
    if i.islower():
        return letter
    else:
        return letter.upper


def print_output(encode_out, output):
    if output == sys.stdout:
        print(encode_out)
    else:
        with open(output, 'w') as file:
            file.write(encode_out)


def select_function(cipher, inp, key, output, decode):
    text = get_text(inp)
    encode_out = str()
    if cipher == 'caesar':
        if decode:
            encode_out = caesar_encryptor(int(key), text, True)
        else:
            encode_out = caesar_encryptor(key, text, False)
    elif cipher == 'vigenere':
        if decode:
            encode_out = vigenere_encryptor(key, text, True)
        else:
            encode_out = vigenere_encryptor(key, text, False)
    print_output(encode_out, output)


def hack(inp, output, model):
    with open(model, 'r') as model_file:
        model_freq = json.load(model_file)
    get_inp = get_text(inp)
    text = count_frequency(get_inp)
    cur_dict = dict()
    min_key = -1
    min_dist = int
    for index in range(len_alph):
        for j in range(len_alph):
            cur_dict[alphabet[j]] = text[alphabet[(j - index) % len_alph]]
        dist = 0
        for alpha in alphabet:
            dist += (model_freq[alpha] - cur_dict[alpha]) ** 2
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
    encode_.add_argument('--input-file', required=False, dest='input', help='Input file', default=sys.stdin)
    encode_.add_argument('--output-file', required=False, dest='output', help='Output file', default=sys.stdout)
    decode_ = subs.add_parser('decode', help='Decode')
    decode_.add_argument('--cipher', help='Cipher')
    decode_.add_argument('--key', dest='key', help='Key')
    decode_.add_argument('--input-file', required=False, dest='input', help='Input file', default=sys.stdin)
    decode_.add_argument('--output-file', required=False, dest='output', help='Output file', default=sys.stdout)
    train_ = subs.add_parser('train', help='Train')
    train_.add_argument('--text-file', required=False,  dest='input', help='Text file', default=sys.stdin)
    train_.add_argument('--model-file', required=True, dest='model', help='Model file')
    hack_ = subs.add_parser('hack', help='Hack')
    hack_.add_argument('--input-file', required=False, dest='input', help='Input file', default=sys.stdin)
    hack_.add_argument('--output-file', required=False, dest='output', help='Output file', default=sys.stdout)
    hack_.add_argument('--model-file', dest='model', help='Model file')
    args = parser.parse_args()
    return args


# -----------------------------------------------------------

# -------------------main------------------------------------


def main():
    args = get_args()
    if args.action == 'encode':
        select_function(args.cipher, args.input, args.key, args.output, False)
    if args.action == 'decode':
        select_function(args.cipher, args.input, args.key, args.output, True)
    if args.action == 'train':
        print_diagram(count_frequency(get_text(args.input)), args.model)
    if args.action == 'hack':
        hack(args.input, args.output, args.model)


if __name__ == '__main__':
    main()
