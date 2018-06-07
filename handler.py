import re
import kbotlib
import json
import random

import parsers.rule34


def handle_msg(msg):
    words = list(filter(None, re.split(r'\s*(\S+)\s*', msg['text'])))
    msg['tags'] = words[1:]
    msg['command'] = words[0]

    if '/hentai' in msg['command']:
        result = parsers.rule34.rule34(msg['tags'])

        start = random.randint(0, len(result))
        attachments = []
        for attach in result[start:start+5]:
            print(attach['type'])
            if attach['type'] == 'photo':
                attachments.append({
                    'type': 'photo',
                    'media': attach['photo'],
                    'caption': ' '.join(attach['tags'][:10])
                })

            elif attach['type'] == 'video':
                attachments.append({
                    'type': 'video',
                    'media': attach['video'],
                    'caption': ' '.join(attach['tags'][:10]),
                })
        print(json.dumps(attachments))
        r = kbotlib.tg_api('sendMediaGroup', {
            'chat_id': msg['chat']['id'],
            'media': json.dumps(attachments)
        })
        print(r)
