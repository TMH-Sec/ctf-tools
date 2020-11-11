#!/usr/bin/env python3
"""
Encode and decode messages embedded in text.
./balanced_stego.py -i injected.txt -d
will print the secret message to screen

./balanced_stego.py -i injected_text.txt -d -o output_file.txt
will print the decoded message to file

./balanced_stego.py -i message.txt -c carrier.txt -o output_file.txt
will make an encoded message
"""
from argparse import ArgumentParser
from functools import reduce
import re


def get_args():
    """
    If encoding, you need -i, -c and -o. If decoding, you need -i and -d.
    When decoding the -o is optional.
    """
    parser = ArgumentParser()
    parser.add_argument('-i', '--in-file', dest='input_file',
                        help='Input file.', required=True)
    parser.add_argument('-c', '--carrier', dest='carrier',
                        help='Carrier message for stego inject.')
    parser.add_argument('-d', '--decode', dest='decode',
                        default=False, action='store_true',
                        help='Use to reverse.')
    parser.add_argument('-o', '--out-file', dest='out_file',
                        help='Output file.')  # if used when decoding, output
    # will not print to screen.
    args = parser.parse_args()
    return args


class BalancedStego:
    """
    My practice class... clunky, but working... ;)
    """
    str2dig = {'+': 1, '-': -1, '0': 0}
    uni2sym = {'\u200b': '-', '\u200c': '0', '\u200d': '+'}
    name2uni = {'zwsp': '\u200b', 'zwnj': '\u200c', 'zwj': '\u200d'}

    @staticmethod
    def turn(number):
        """Converts individual decimal number to balanced ternary"""
        if number == 0:
            return []
        if number % 3 == 0:
            return [0] + BalancedStego.turn(int(number // 3))
        if number % 3 == 1:
            return [1] + BalancedStego.turn(int(number // 3))
        if number % 3 == 2:
            return [-1] + BalancedStego.turn(int((number + 1) // 3))

    @staticmethod
    def format_turned(turned_list):
        """Formats the pre-balanced ternary, for internal reference."""
        turned = ''
        for char in reversed(range(0, len(turned_list))):
            if turned_list[char] == -1:
                turned += '-'
            if turned_list[char] == 0:
                turned += '0'
            if turned_list[char] == 1:
                turned += '+'
        return turned

    @staticmethod
    def collect_message(raw_message):
        """For convolution's sake."""
        collected_message = []
        for char in raw_message:
            collected_message.append(char)
        return collected_message

    @staticmethod
    def change_case(message_collected):
        """From ascii to decimal, one character at a time."""
        res = ';'.join(format(ord(char), 'd') for char in message_collected)
        changed = res.split(';')
        return changed

    @staticmethod
    def make_it(intermediate_message):
        """I love convolution"""
        different = []
        for k in intermediate_message:
            stuff = BalancedStego.turn((int(k)))
            different.append(BalancedStego.format_turned(stuff))
        return different

    @staticmethod
    def make_magic(changed_list):
        """
        Sometimes, when you just glue to scripts together into a class, it
        may not make any sense.
        """
        magic_list = []
        for char1 in changed_list:
            temp = ''
            also_temp = str(char1)
            if also_temp != '+0+':
                for char2 in also_temp:
                    if char2 == '0':
                        temp += BalancedStego.name2uni['zwnj']
                    if char2 == '+':
                        temp += BalancedStego.name2uni['zwj']
                    if char2 == '-':
                        temp += BalancedStego.name2uni['zwsp']
                magic_list.append(temp)
        return magic_list

    @staticmethod
    def inject(infile, list_of_magic):
        """
        Takes the encoded text and injects characters that are normally not
        printed.
        """
        dumby = BalancedStego.get_from_file(infile)
        final = ''
        counter = 0
        for index in range(0, len(dumby) - 1):
            character = dumby[index]
            final += str(character)
            if dumby[index] != ' ':
                if dumby[index] != '\n':
                    if dumby[index + 1] != ' ':
                        if dumby[index + 1] != '\n':
                            try:
                                final += list_of_magic[counter]
                                counter += 1
                            except IndexError:
                                final += dumby[index + 1:]
                                break
        return final

    @staticmethod
    def get_from_file(infile):
        """Returns all characters from a file."""
        file = open(infile, 'r')
        stuff = file.read()
        file.close()
        return stuff

    @staticmethod
    def write_to_file(outfile, magic_text):
        """Writes all characters to a file."""
        file = open(outfile, 'w')
        for char in magic_text:
            file.write(char)
        file.close()

    @staticmethod
    def read_the_shit(strings):
        """Collect all appropriate symbols for decoding."""
        result = ''
        for char in strings:
            if char == '\n':
                result += ' '
            elif not char.isprintable():
                result += BalancedStego.uni2sym[char]
            else:
                result += ' '
        result = result.strip()
        return result

    @staticmethod
    def un_turn(r_string):
        """Return balanced ternary to decimal."""
        dig = [BalancedStego.str2dig[char] for char in reversed(r_string)]
        return reduce(lambda var1, var2: var2 + 3 * var1, reversed(dig), 0)

    @staticmethod
    def do_it(file):
        """Write decoded text to screen."""
        stuff = BalancedStego.get_from_file(file)
        res = BalancedStego.read_the_shit(stuff)
        res_list = res.split()
        final = ''
        for item in res_list:
            s_item = str(item).strip('\n')
            d_item = BalancedStego.un_turn(s_item)
            is_item = str(d_item)
            str_item = re.search(r'\d+', is_item)
            final += chr(int(str_item.group(0)))
        print(final)

    @staticmethod
    def do_it_to_file(file, out_file):
        """Write decoded text to file."""
        stuff = BalancedStego.get_from_file(file)
        res = BalancedStego.read_the_shit(stuff)
        res_list = res.split()
        final = ''
        for item in res_list:
            s_item = str(item).strip('\n')
            d_item = BalancedStego.un_turn(s_item)
            is_item = str(d_item)
            str_item = re.search(r'\d+', is_item)
            final += chr(int(str_item.group(0)))
        file = open(out_file, 'w')
        file.write(final)
        file.close()


if __name__ == '__main__':
    ARGUMENTS = get_args()
    if ARGUMENTS.decode is False:
        MESSAGE = BalancedStego.get_from_file(ARGUMENTS.input_file)
        COLLECTED = BalancedStego.collect_message(MESSAGE)
        CASE = BalancedStego.change_case(COLLECTED)
        MADE = BalancedStego.make_it(CASE)
        TRY_ME = BalancedStego.make_magic(MADE)
        REALLY_NOW = BalancedStego.inject(ARGUMENTS.carrier, TRY_ME)
        BalancedStego.write_to_file(ARGUMENTS.out_file, REALLY_NOW)
    elif ARGUMENTS.decode and ARGUMENTS.out_file:
        BalancedStego.do_it_to_file(ARGUMENTS.input_file, ARGUMENTS.out_file)
    elif ARGUMENTS.decode and not ARGUMENTS.out_file:
        BalancedStego.do_it(ARGUMENTS.input_file)
    else:
        print('you messed up.')
