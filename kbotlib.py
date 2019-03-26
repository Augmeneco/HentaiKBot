import requests 
import json
from datetime import datetime

TG_TOKEN = json.loads(open('./config.json').read())['token']


def log_print(text, type='info'):
    print('[' + datetime.now().strftime("%H:%M:%S") + '] ' + text)


def tg_api(method, parameters={}, token=TG_TOKEN, file=None):
    tor = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }
    url = 'https://api.telegram.org/bot' + token + '/' + method
    headers = {}

    # if method.split('.')[1][:3] == 'get':
    if file is None:
        r = requests.post(url, params=parameters, headers=headers, proxies=tor)
    else:
        r = requests.post(url, params=parameters, headers=headers, proxies=tor, files={'file': file})
    # print(r.text)
    return r.json()
