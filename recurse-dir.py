from subprocess import check_output
from re import search
from argparse import ArgumentParser


def get_arguments():
    parser = ArgumentParser()
    parser.add_argument('-u', '--url', dest='url', help='url e.g. http://127.0.0.1:80')
    parser.add_argument('-w', '--word-list', dest='word_list', help='path to word list, hrm with no #`s at all mkay')
    parser.add_argument('-d', '--directory', dest='directory', help='known directory to look in')
    parser.add_argument('-e', '--extension', dest='extension', help='extension to use with word list')
    arguments = parser.parse_args()
    return arguments


def read_line(path):
    with open(path) as file:
        lines = file.read().splitlines()
        return lines  # list


def curl_it(url, directory, word, extension):
    curl_result = check_output('curl {}/{}/{}.{}'.format(url, directory, word, extension), shell=True)
    curl_result = str(curl_result)
    yeah = search(r'404', curl_result)
    if not yeah:
        out_file.write('[+] 200 {}/{}/{}.{}\n'.format(url, directory, word, extension))
        print('[+] 200 {}/{}/{}.{}'.format(url, directory, word, extension))
    else:
        print('[-] damn {}/{}/{}.{}'.format(url, directory, word, extension))


with open('output_of_recurse_dir.py.txt', 'a') as out_file:
    arguments_list = get_arguments()
    words = read_line(arguments_list.word_list)
    for w0rd in words:
        curl_it(arguments_list.url, arguments_list.directory, w0rd, arguments_list.extension)
    out_file.close()
