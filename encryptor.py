import sys
import string
import argparse
import json


alphabet = string.ascii_lowercase
ALPHABET = string.ascii_uppercase
lenAlph = len(alphabet)


def get_text(input_file):
    if input_file == sys.stdin:
        text = input()
    else:
        file = open(input_file, 'r')
        text = file.read()
    return text


def count_frequency(text):
    model = dict()
    alpha_count = 0
    for i in alphabet:
        model[i] = 0
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
        file = open(out, 'w')
        file.write(json.dumps(dict_))


def encode_caesar(key, text):
    out = str()
    for i in text:
        if i.islower():
            out += (alphabet[(alphabet.find(i) + int(key)) % lenAlph])
        elif i.isupper():
            out += (ALPHABET[(ALPHABET.find(i) + int(key)) % lenAlph])
        else:
            out += i
    return out


def encode_vigenere(key, text):
    out = str()
    new_key = key * (len(text) // len(key) + 1)
    for i in range(len(text)):
        if text[i].islower():
            out += (alphabet[(alphabet.find(text[i]) + alphabet.find(new_key.lower()[i])) % lenAlph])
        elif text[i].isupper():
            out += (ALPHABET[(ALPHABET.find(text[i]) + ALPHABET.find(new_key.upper()[i])) % lenAlph])
        else:
            new_key = new_key[:i] + ' ' + new_key[i:]
            out += (text[i])
    return out


def decode_caesar(key, text):
    out = str()
    for i in text:
        if i.islower():
            t = alphabet.find(i) - key
            if t < 0:
                t += lenAlph
            out += (alphabet[t % lenAlph])
        elif i.isupper():
            t = ALPHABET.find(i) - key
            if t < 0:
                t += lenAlph
            out += (ALPHABET[t % lenAlph])
        else:
            out += i
    return out


def decode_vigenere(key, text):
    out = str()
    new_key = key * (len(text) // len(key) + 1)
    for i in range(len(text)):
        if text[i].islower():
            t = alphabet.find(text[i]) - alphabet.find(new_key.lower()[i])
            if t < 0:
                t += lenAlph
            out += (alphabet[t % lenAlph])
        elif text[i].isupper():
            t = ALPHABET.find(text[i]) - ALPHABET.find(new_key.upper()[i])
            if t < 0:
                t += lenAlph
            out += (ALPHABET[t % lenAlph])
        else:
            new_key = new_key[:i] + ' ' + new_key[i:]
            out += (text[i])
    return out


def encode(cipher, inp, key, output):
    text = get_text(inp)
    encode_out = str()
    if cipher == 'caesar':
        encode_out = encode_caesar(key, text)
    elif cipher == 'vigenere':
        encode_out = encode_vigenere(key, text)
    if output == sys.stdout:
        print(encode_out)
    else:
        file = open(output, 'w')
        file.write(encode_out)


def decode(cipher, inp, key, output):
    text = get_text(inp)
    if cipher == 'caesar':
        encode_out = decode_caesar(int(key), text)
    elif cipher == 'vigenere':
        encode_out = decode_vigenere(key, text)
    if output == sys.stdout:
        print(encode_out)
    else:
        file = open(output, 'w')
        file.write(encode_out)


def hack(inp, output, model):
    with open(model, 'r') as model_file:
        model_freq = json.load(model_file)
    get_inp = get_text(inp)
    text = count_frequency(get_inp)
    cur_dict = dict()
    min_dist = lenAlph
    min_key = 0
    for index in range(lenAlph):
        for j in range(lenAlph):
            cur_dict[alphabet[j]] = text[alphabet[(j - index) % lenAlph]]
        dist = 0
        for alpha in alphabet:
            dist += model_freq[alpha] - cur_dict[alpha]
        if dist < min_dist:
            min_dist = dist
            min_key = index
    code = encode_caesar(min_key, get_inp)
    if output == sys.stdout:
        print(code)
    else:
        file = open(output, 'w')
        file.write(code)
# ---------------------------------------------------


def get_args():
    action = None
    cipher = None
    key = None
    inp = None
    output = None
    text = None
    model = None
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
        encode(args.cipher, args.input, args.key, args.output)
    if args.action == 'decode':
        decode(args.cipher, args.input, args.key, args.output)
    if args.action == 'train':
        print_diagram(count_frequency(get_text(args.input)), args.model)
    if args.action == 'hack':
        hack(args.input, args.output, args.model)


if __name__ == '__main__':
    main()
