import json, random, string, hashlib, requests, threading, time, sys, argparse
from load_settings_funcs import load_settings, load_data, load_proxies_for_getting_cookies, load_user_agents_for_getting_cookies
from settings_data import SettingsData, settings_dict
import work_with_net as wwn
import get_cookies
from itertools import cycle
from network_classes import Proxy
from settings_data import Cookie


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


def reg_account_wrapper(i, print_status_code, new_tech_data, get_cookies_from_request=False, save_with_user_agent=False, proxy_for_getting_cookie=None, u_agent_for_getting_cookie=None):
    repeat_reg = False
    user_agent = wwn.generate_user_agent(SettingsData.devices, SettingsData.locales)
    guid = wwn.generate_guid()
    guid2 = wwn.generate_guid()
    guid3 = wwn.generate_guid()
    adid = wwn.generate_guid()
    device_id = wwn.generate_device_id()
    name = random.choice(SettingsData.names)
    surname = random.choice(SettingsData.surnames)

    if get_cookies_from_request:
        # cookie = get_cookies.get_cookie(proxy_for_getting_cookie, u_agent_for_getting_cookie)

        th = ThreadWithReturnValue(target=get_cookies.get_cookie, args=(proxy_for_getting_cookie, u_agent_for_getting_cookie))
        th.start()
        cookie = th.join()
        # print('# {}, getting new cookie Proxy:{} uagent:{}'.format(i, proxy_for_getting_cookie, u_agent_for_getting_cookie))
        # print('ONE: ', cookie)
        # with open('cookie_log.txt', 'a') as f:
        #     f.write('1;' + str(cookie) + '\n')

        # with open('data/cookies.txt') as f:
        #     raw_cookies = [line.strip() for line in f.readlines()]
        # raw_cookie = random.choice(raw_cookies)
        # cookie = Cookie(raw_cookie.split(';')[0], raw_cookie.split(';')[1], raw_cookie.split(';')[2], raw_cookie.split(';')[3])
        # print(cookie)
        # # time.sleep(10)
        # # cookie = Cookie(raw_cookie.split(';')[0], raw_cookie.split(';')[1], raw_cookie.split(';')[2], raw_cookie.split(';')[3])
        # print('TWO: ', cookie)
    else:
        cookie = SettingsData.cookies[i]
        # with open('cookie_log.txt', 'a') as f:
        #     f.write('2;' + str(cookie) + '\n')

    if not cookie:
        print("cant't get cookie from proxy:", proxy_for_getting_cookie)
        return
    # print(get_cookies_from_request, cookie)
    gen_str = ''
    if settings_dict['gen_str_for_proxy']:
        gen_str = wwn.gen_str_for_proxy_to_add_to_login()

    pr = Proxy(SettingsData.proxies[0].ip, SettingsData.proxies[0].port, SettingsData.proxies[0].login+gen_str, SettingsData.proxies[0].pw)
    import importlib
    importlib.reload(requests)
    with requests.Session() as s:
        while True:
            if not reg_account(s, i, pr, print_status_code, new_tech_data, cookie, name, surname, guid, guid2, guid3, adid, device_id, user_agent, repeat_reg, save_with_user_agent):
                break
            else:
                repeat_reg = True
                time.sleep(5)


def reg_account(session, i, proxy, print_status_code, new_tech_data, cookie, name, surname, guid, guid2, guid3, adid, device_id, user_agent, repeat, save_with_user_agent=False):
    if new_tech_data:
        user_agent = wwn.generate_user_agent(SettingsData.devices, SettingsData.locales)
        guid = wwn.generate_guid()
        guid2 = wwn.generate_guid()
        guid3 = wwn.generate_guid()
        adid = wwn.generate_guid()
        device_id = wwn.generate_device_id()

    account_created = False

    mail = wwn.generate_mail(name)
    username = wwn.generate_username(mail)

    sn_nonce = wwn.generate_sn_nonce(mail)
    pw = wwn.generate_pw()

    data = wwn.generate_data(guid, guid2, guid3, adid, cookie.csrftoken, username, surname, device_id, mail, sn_nonce, pw)

    encrypted_data = wwn.encrypt_data_sha256(data)
    url_encoded_data = wwn.url_encode(data)

    try:
        resp = wwn.reg_request(proxy, user_agent, cookie, encrypted_data, url_encoded_data, session, SettingsData.proxies, i, repeat)
        # print(resp.text)
        # print()
        if print_status_code:
            print('# {}. HTPP status code: {}'.format(i, resp.status_code))
        if 'created_user' in json.loads(resp.text):
            account_created = True
            if resp.ok:
                print('ok # {}'.format(i))
                import winsound
                winsound.Beep(300, 700)


            # print(json.loads(resp.text))
            ds_user_id = json.loads(resp.text)['created_user']['pk']
            with open('goods.txt', 'a') as f:
                u_agent_to_save = user_agent if save_with_user_agent else ''
                text_to_save = '{username}:{pw}|{u_agent_to_save}|{device_id};{guid2};{guid};{adid}|ds_user={username};' \
                               'rur={rur};mid={mid};csrftoken={csrftoken};ds_user_id={ds_user_id};' \
                               'sessionid={session_id};is_starred_enabled=yes;urlgen=;||'.format(username=username, pw=pw,
                                                        device_id=device_id,
                                                        guid2=guid2, guid=guid, adid=adid,
                                                        rur=cookie.rur,
                                                        mid=cookie.mid,
                                                        csrftoken=cookie.csrftoken,
                                                        ds_user_id=ds_user_id,
                                                        session_id=session.cookies.get_dict()['sessionid'],
                                                        u_agent_to_save=u_agent_to_save)
                f.write(text_to_save)
                f.write('\n')

    except requests.exceptions.ProxyError:
        print('requests.exceptions.ProxyError #', i)
    except Exception as e:
        print(str(e))


    #
    # finally:
    #     return account_created


if __name__ == '__main__':
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

    my_args = parser.parse_args()
    number_of_threads = my_args.number_of_threads
    number_of_iterations = my_args.iters
    print_status_code = my_args.status_code
    delete_used_cookies = my_args.delete_used_cookies
    new_tech_data = my_args.new_tech_data
    infinite_iterations = True if number_of_iterations == -1 else False
    cookie_from_request = my_args.cookies_from_request
    save_with_user_agent = my_args.save_with_user_agent
    load_settings()

    number_of_iterations = load_data(number_of_iterations, delete_used_cookies, cookie_from_request)

    print_timeout = 10
    if number_of_threads >= 50:
        print_timeout *= 2.5
        if number_of_threads >= 100:
            print_timeout *= 2

    if cookie_from_request:
        load_proxies_for_getting_cookies()
        load_user_agents_for_getting_cookies()
        if number_of_iterations == -1:
            number_of_iterations = 1000000

    while True:
        proxy_u_agent = cycle(range(1))
        if cookie_from_request:
            proxy_u_agent = zip(cycle(SettingsData.proxies_for_getting_cookies), cycle(SettingsData.user_agents_for_getting_cookies))
        # print('number_of_iterations - ', number_of_iterations)
        for i, data in zip(range(number_of_iterations), proxy_u_agent):
            # print (data)
            # time.sleep(99)
            # print("$ ", i)
            while len(threading.enumerate()) - 1 >= number_of_threads:
                time.sleep(0.001)
            if cookie_from_request:
                proxy_for_getting_cookie = Proxy(data[0].split(':')[0], data[0].split(':')[1])
                th = threading.Thread(target=reg_account_wrapper, args=(i, print_status_code,
                                                                        new_tech_data,
                                                                        cookie_from_request,
                                                                        save_with_user_agent,
                                                                        proxy_for_getting_cookie,
                                                                        data[1]))
            else:
                # print('no')
                th = threading.Thread(target=reg_account_wrapper, args=(i, print_status_code,
                                                                        new_tech_data,
                                                                        cookie_from_request,
                                                                        save_with_user_agent))
            th.start()

            if i % print_timeout == 0:
                print('iters: ', i)
                print('threads: ', len(threading.enumerate())-1)

        if not infinite_iterations:
            break
