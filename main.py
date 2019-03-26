import time
import queue
import threading
import kbotlib
import handler
import os


updates_queue = queue.Queue()


def longpollserver():
    last_update_id = 0

    while True:
        time.sleep(10/ 1000000.0)

        res = kbotlib.tg_api('getUpdates', parameters={'timeout': 100,'offset': last_update_id + 1})
        if res['result'] == []:
            continue

        last_update_id = res['result'][-1]['update_id']

        for update in res['result']:
            updates_queue.put(update)


if __name__ == '__main__':

    kbotlib.log_print('Запуск longpoll потока ...')
    thread_longpoll = threading.Thread(target=longpollserver)
    thread_longpoll.start()
    kbotlib.log_print('Longpoll поток запущен.')
    try:
        while True:
            time.sleep(10 / 1000000.0)
            update = updates_queue.get()
            if 'message' in update:
                msg = update['message']
                threading.Thread(target=handler.handle_msg, args=(msg,)).start()
    except KeyboardInterrupt:
        os._exit(0)
