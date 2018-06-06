import requests
import time
import json
from datetime import datetime
import re
import queue
import threading


TG_TOKEN = '559554306:AAHtWdl0uFMavh7LTCF_r40rMeF3eU0x0Zg'

updates_queue = queue.Queue()


def log_print(text, type='info'):
    print('[' + datetime.now().strftime("%H:%M:%S") + '] ' + text)


def tg_api(method, parameters={}, token=TG_TOKEN, file=None):
    url = 'https://api.telegram.org/bot' + token + '/' + method
    headers = {}

    #if method.split('.')[1][:3] == 'get':
    if file == None:
        r = requests.post(url, params=parameters, headers=headers)
    else:
        r = requests.post(url, params=parameters, headers=headers, files={'file': file})
    # print(r.text)
    return r.json()


def longpollserver():
    res = tg_api('getUpdates', parameters={'offset': -1})
    last_update_id = res['result'][-1]['update_id']

    while True:
        time.sleep(10 / 1000000.0)

        res = tg_api('getUpdates', parameters={'offset': last_update_id + 1})
        if res['result'] == []:
            continue

        last_update_id = res['result'][-1]['update_id']

        for update in res['result']:
            updates_queue.put(update)


if __name__ == '__main__':
    log_print('Запуск longpoll потока ...')
    thread_longpoll = threading.Thread(target=longpollserver)
    thread_longpoll.start()
    log_print('Longpoll поток запущен.')

    while True:
        time.sleep(10 / 1000000.0)
        update = updates_queue.get()
        print(update)
