import re
import kbotlib
import json
import random

import parsers.rule34


def handle_msg(msg):
    msg['pretty_text'] = msg['text'].replace('+', ' ')
    words = list(filter(None, re.split(r'\s*(\S+)\s*', msg['pretty_text'])))
    msg['tags'] = words[1:]
    msg['command'] = words[0]

    if '!all' in msg['tags'].lower():
        msg['tags'].extend({'-fur','-pony*','-friendship*','-scat*','-furry','-dragon','-guro','-animal_penis','-animal','-wolf','-fox','-webm','-my_little_pony','-monster*','-3d','-animal*','-ant','-insects','-mammal','-horse','-blotch','-deer','-real*','-shit','-everlasting_summer','-copro*','-wtf'})

    if '/hentai' in msg['command']:
        result = parsers.rule34.rule34(msg['tags'])

        random.shuffle(result)

        start = random.randint(0, len(result))
        attachments = []
        for attach in result[start:start + 5]:
            if 'url' in attach:
                print(attach['url'])

            if attach['type'] == 'photo':
                attachments.append({
                    'type': 'photo',
                    'media': attach['url'],
                    'caption': ' '.join(attach['tags'])[0:199]
                })

            elif attach['type'] == 'video':
                attachments.append({
                    'type': 'video',
                    'media': attach['url'],
                    'caption': ' '.join(attach['tags'])[0:199],
                })

        if attachments != []:
            tg_resp = kbotlib.tg_api('sendMediaGroup', {
                'chat_id': msg['chat']['id'],
                'media': json.dumps(attachments)
            })
            if tg_resp['ok'] is True:
                kbotlib.log_print('MsgID#' + str(msg['message_id']) + ': Запрос успешно обработан')
            else:
                kbotlib.log_print('MsgID#' + str(msg['message_id']) + ': Error:' + tg_resp['description'])
        else:
            kbotlib.log_print('MsgID#' + str(msg['message_id']) + ': Ничего не найдено')
            kbotlib.tg_api('sendMessage', {
                'chat_id': msg['chat']['id'],
                'text': 'По вашему запросу ничего не найдено!',
                'reply_to_message_id': msg['message_id']
            })
