import json, random, string, hashlib, requests, threading, time, sys, argparse
# from load_settings import load_settings, load_data, load_proxies_for_getting_cookies, load_user_agents_for_getting_cookies
import load_settings
from settings_data import SettingsData
import work_with_net as wwn
import get_cookies
from itertools import cycle, count
from instagram import Proxy, Instagram


class ThreadWithReturnValue(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        # print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)

    def join(self):
        threading.Thread.join(self)
        return self._return


def make_command_line_args():
    parser = argparse.ArgumentParser(description='my args')
    parser.add_argument('number_of_threads', type=int, help='number of threads')

    parser.add_argument('--iters', type=int, default=-1,
                        help='iterations (если не указывать, токоличество итераций будет бесконечным)')

    parser.add_argument('--delete_used_cookies', type=bool, default=False,
                        help='удаление использованных куки из файла')

    parser.add_argument('--status_code', type=bool, default=False,
                        help='выводить status code от серверва')

    parser.add_argument('--new_tech_data', type=bool, default=False,
                        help='генерировать новые тех данные при повторной попытке регистрации')

    parser.add_argument('--cookies_from_request', type=bool, default=False,
                        help='получать куки не из файла, а из запросов')

    parser.add_argument('--save_with_user_agent', type=bool, default=False,
                        help='сохранять user-agent')

    parser.add_argument('--save_in_json', type=bool, default=False,
                        help='создавать json файл с аккаунтами')

    parser.add_argument('--set_bio', type=bool, default=False,
                        help='Изменять биографию')

    parser.add_argument('--subscribe', type=bool, default=False,
                        help='Подписаться на юзеров')

    parser.add_argument('--device_id_from_file', type=bool, default=False,
                        help='Брать device_id из файла')

    d = parser.parse_args().__dict__
    d['number_of_iterations'] = d.pop('iters')
    d['print_status_code'] = d.pop('status_code')
    return d


def main():

    args = make_command_line_args()
    infinite_iterations = True if args['number_of_iterations'] == -1 else False
    settings = load_settings.load_settings()
    args['gen_str_for_proxy'] = settings['gen_str_for_proxy']
    proxies = load_settings.load_proxies(settings)

    names = load_settings.load_names(settings)
    surnames = load_settings.load_surnames(settings)
    locales = load_settings.load_locales(settings)
    devices = load_settings.load_devices(settings)
    cookies = load_settings.load_cookies(settings, args['number_of_iterations'], args['delete_used_cookies'])

    print_timeout = 10
    if args['number_of_threads'] >= 50:
        print_timeout *= 2.5
        if args['number_of_threads'] >= 100:
            print_timeout *= 2

    if args['cookies_from_request']:
        proxies_for_getting_cookies = load_settings.load_proxies_for_getting_cookies(settings)
        user_agents_for_getting_cookies = load_settings.load_user_agents_for_getting_cookies(settings)
        # if args['number_of_iterations'] == -1:
        #     number_of_iterations = 1000000
        proxy_u_agent_for_gettin_cookies = zip(cycle(proxies_for_getting_cookies), cycle(user_agents_for_getting_cookies))

    iters = range(args['number_of_iterations']) if args['number_of_iterations'] !=-1 else count()

    for i, cookie, name, surname, device, locale, proxy\
            in zip(iters, cycle(cookies), cycle(names), cycle(surnames), cycle(devices), cycle(locales), cycle(proxies)):
        while len(threading.enumerate()) - 1 >= args['number_of_threads']:
            time.sleep(0.001)

        user_agent = Instagram.generate_user_agent(settings, devices, locales)

        if args['cookies_from_request']:
            raw_proxy, u_agent = next(proxy_u_agent_for_gettin_cookies)
            # print(raw_proxy)
            # time.sleep(100)
            proxy_for_cookie = Proxy(raw_proxy.split(':')[0], raw_proxy.split(':')[1])

            th = ThreadWithReturnValue(target=Instagram.get_cookie_from_request,
                                       args=(proxy_for_cookie, u_agent))
            th.start()
            cookie = th.join()

            # cookie = Instagram.get_cookie_from_request(proxy, u_agent)

        if cookie:
            # print(cookie)
            insta = Instagram(args, settings, proxy, cookie, user_agent, name, surname, device, locale, i)
            insta.start()
        else:
            print('get_cookie_from_request error #', i)

        if i % print_timeout == 0:
                print('iters: ', i)
                print('threads: ', len(threading.enumerate()) - 1)


if __name__ == '__main__':
    main()
