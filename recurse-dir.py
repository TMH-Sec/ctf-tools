from subprocess import check_output
from re import search
from argparse import ArgumentParser


def get_arguments():
    parser = ArgumentParser()
    parser.add_argument('-u', '--url', dest='url', help='url e.g. http://127.0.0.1:80')
    parser.add_argument('-w', '--word-list', dest='word_list', help='path to word list')
    parser.add_argument('-d', '--directory', dest='directory', help='known directory to look in')
    parser.add_argument('-e', '--extension', dest='extension', help='extension to use with word list')
    arguments = parser.parse_args()
    return arguments


def read_line(path):
    with open(path) as file:
        lines = file.read().splitlines()
        return lines  # list


def curl_it(url, word, directory, extension):
    curl_result = check_output('curl {}/{}/{}.{}'.format(url, directory, word, extension), shell=True)
    curl_result = str(curl_result)
    yeah = search(r'200', curl_result)
    if yeah:
        print('[+] 200 {}/{}/{}.{}'.format(url, directory, word, extension))


arguments_list = get_arguments()
words = read_line(arguments_list.word_list)
for w0rd in words:
    curl_it(arguments_list.url, w0rd, arguments_list.directory, arguments_list.extension)
