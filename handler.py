import re
import kbotlib
import json
import random
# parsers
import parsers.rule34
import parsers.booru


TAGS_BLACKLIST = json.loads(open('./config.json').read())['tags_blacklist']


def handle_msg(msg):
    kbotlib.log_print('MsgID#' + str(msg['message_id']) + ' Начало обработки запроса')
    msg['pretty_text'] = msg['text'].replace('+', ' ').lower()
    words = list(filter(None, re.split(r'\s*(\S+)\s*', msg['pretty_text'])))
    msg['tags'] = words[1:]
    msg['command'] = words[0]

    print(msg['tags'])

    if '/hentai' in msg['command']:
        if '!rtrd' not in msg['tags']:
            msg['tags'].extend(TAGS_BLACKLIST)
        else:
            msg['tags'].remove('!rtrd')

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

    elif '/animeart' in msg['command']:
        result = parsers.booru.booru(msg['tags'])

        random.shuffle(result)

        start = random.randint(0, len(result))
        attachments = []
        for attach in result[start:start + 5]:
            # if 'url' in attach:
            #     print(attach['url'])

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
