import requests
from time import sleep
from threading import Thread
# from proxies import proxies
from proxies2 import pr2
import os

class SpamThread(Thread):
    def __init__(self, id, times, proxy):
        Thread.__init__(self)
        self.times = times
        self.id = id
        self.proxy = proxy
        self.spam_on = True

    def run(self):
            step = 1000
            # print('THREAD START: ', self.id)
            try:
                for i in range(self.times):

                        mproxies = {
                            "http": "socks4://{}".format(self.proxy),
                        }
                        resp = requests.get('http://jsonip.com', proxies=mproxies)
                        if i % step == 0:
                            print('spam: # {}, code:{}, id: {} '.format(i, resp.status_code, self.id))
                        sleep(0.2)
            except:
                # print('except')
                pass
            # print('THREAD STOP')

            self.spam_on = False


class SpamThreadsDaddy(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.spam_threads = []

    def add_thread(self, thread):
        self.spam_threads.append(thread)

    def run(self):
        while True:
            stopped_threads = filter(lambda x: not x.spam_on, self.spam_threads)
            for stopped in stopped_threads:
                # print(stopped.spam_on)
                # print('removed stopped thread')
                self.spam_threads.remove(stopped)
            # print(os.system('CLS'))
            print('THREADS: ', self.number_of_threads())
            sleep(1)

    def is_spamming(self, client, phone=None):
        spamming = False
        for thr in self.spam_threads:
            if phone:
                if thr.client == client and thr.phone == phone:
                    spamming = True
            else:
                if thr.client == client:
                    spamming = True
        return spamming

    def stop_spam(self, client):
        for thr in self.spam_threads:
            if thr.client == client:
                thr.spam_on = False

    def number_of_threads(self):
        return len(self.spam_threads)

spam_threads = SpamThreadsDaddy()

spam_threads.start()

for i in range(len(pr2)):
    while spam_threads.number_of_threads() > 500:
        sleep(1)
    thr = SpamThread(i, 100000, pr2[i])
    thr.start()
    spam_threads.add_thread(thr)

    # sleep(0.1)

# resp = requests.get('http://wiolex.ru')
# print(resp.status_code)