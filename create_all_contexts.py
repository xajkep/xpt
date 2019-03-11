#!/usr/bin/python
# coding: utf-8
import json

CONTEXTS_FILE = "contexts.json"
SERVER_PATH = "server"

HTML_DOCUMENT = """<!DOCTYPE>
<html>
<head>
%s
</head>
<body>
%s
</body>
</html>
"""

VULNERABLE_PHP_CODE = """<?php
$c = $_GET['c'];
%s
echo $c;
?>"""

EXTERNAL_VULNERABLE_PHP_CODE = """<?php
$c = "1337";
%s
file_put_contents(__DIR__.'/tmp.php', $c);
?>
<script src='tmp.php'></script>"""

PHP_URLENCODE = "$c = urlencode($c);"
PHP_HTMLESCAPE = "$c = htmlentities($c, ENT_QUOTES);"

contexts = json.loads(open(CONTEXTS_FILE, 'r').read())['contexts']

file_content = ''
for context in contexts:

    php_transform = ''
    if context['urlencode']:
        php_transform = PHP_URLENCODE
    elif context['htmlescape']:
        php_transform = PHP_HTMLESCAPE
    
    quote = '"'
    external = True
    try:
        if context['external']:
            if context['code'].count('"') >= 2:
                vuln_code = EXTERNAL_VULNERABLE_PHP_CODE.replace('"', "'")
                quote = "'"
            else:
                vuln_code = EXTERNAL_VULNERABLE_PHP_CODE

            php_code = vuln_code % (php_transform)
            code = context['code'].replace('injection', "%s.$_GET['c'].%s" % (quote,quote))
            code = php_code.replace('1337', code)
        else:
            external = False          
    except Exception as e:
        external = False
        pass

    if not external:
        php_code = VULNERABLE_PHP_CODE % (php_transform)
        code = context['code'].replace('injection', php_code)
    
    if context['inhead']:
        head = code
        body = ''
    else:
        head = ''
        body = code
    
    file_path = "%s/%s.php" % (SERVER_PATH, context['name'])
    file_content = HTML_DOCUMENT % (head, body)

    print("Writing %s" % file_path)
    fd = open(file_path, 'w')
    fd.write(file_content)
    fd.close()

