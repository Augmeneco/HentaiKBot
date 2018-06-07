import re

import rule34


def handle_msg(msg):
    words = filter(None, re.split(r'\s*(\S+)\s*', msg['text']))
    msg['tags'] = words[1:]
    msg['command'] = words[1]

    if msg['command'] == '/hentai':
        result = rule34(msg['tags'])

        for item in result:
            
