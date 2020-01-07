import json, random, string, hashlib, requests, threading, time, sys, argparse
from load_settings_funcs import load_settings, load_data
from settings_data import SettingsData
import work_with_net as wwn


def reg_account_wrapper(i, print_status_code, new_tech_data):
    repeat_reg = False
    user_agent = wwn.generate_user_agent(SettingsData.devices, SettingsData.locales)
    guid = wwn.generate_guid()
    guid2 = wwn.generate_guid()
    guid3 = wwn.generate_guid()
    adid = wwn.generate_guid()
    device_id = wwn.generate_device_id()
    with requests.Session() as s:
        while True:
            # if try_reg > 0:
            #     repeat_reg = True
            if not reg_account(s, i, print_status_code, new_tech_data, guid, guid2, guid3, adid, device_id, user_agent, repeat_reg):
                break
            else:
                repeat_reg = True
                time.sleep(5)
            # try_reg += 1
            # if try_reg >= next:
            #     break


def reg_account(session, i, print_status_code, new_tech_data, guid, guid2, guid3, adid, device_id, user_agent, repeat):
    if new_tech_data:
        user_agent = wwn.generate_user_agent(SettingsData.devices, SettingsData.locales)
        guid = wwn.generate_guid()
        guid2 = wwn.generate_guid()
        guid3 = wwn.generate_guid()
        adid = wwn.generate_guid()
        device_id = wwn.generate_device_id()

    account_created = False

    csrftoken = SettingsData.cookies[i].csrftoken
    mail = wwn.generate_mail(SettingsData.names[i])
    username = wwn.generate_username(mail)
    surname = SettingsData.surnames[i]

    sn_nonce = wwn.generate_sn_nonce(mail)
    pw = wwn.generate_pw()

    data = wwn.generate_data(guid, guid2, guid3, adid, csrftoken, username, surname, device_id, mail, sn_nonce, pw)
    encrypted_data = wwn.encrypt_data_sha256(data)
    url_encoded_data = wwn.url_encode(data)

    try:
        resp = wwn.reg_request(user_agent, SettingsData.cookies[i], encrypted_data, url_encoded_data, session, SettingsData.proxies, i, repeat)
        if print_status_code:
            print('# {}. HTPP status code: {}'.format(i, resp.status_code))
        if 'created_user' in json.loads(resp.text):
            account_created = True
            if resp.ok:
                print('ok # {}'.format(i))пш
            # print(json.loads(resp.text))
            ds_user_id = json.loads(resp.text)['created_user']['pk']
            with open('goods.txt', 'a') as f:
                text_to_save = '{username}:{pw}||{device_id};{guid2};{guid};{adid}|ds_user={username};' \
                               'rur={rur};mid={mid};csrftoken={csrftoken};ds_user_id={ds_user_id};' \
                               'sessionid={session_id};is_starred_enabled=yes;urlgen=;||'.format(username=username, pw=pw,
                                                        device_id=device_id,
                                                        guid2=guid2, guid=guid, adid=adid,
                                                        rur=SettingsData.cookies[i].rur,
                                                        mid=SettingsData.cookies[i].mid,
                                                        csrftoken=SettingsData.cookies[i].csrftoken,
                                                        ds_user_id=ds_user_id,
                                                        session_id=session.cookies.get_dict()['sessionid'])
                f.write(text_to_save)
                f.write('\n')

    except requests.exceptions.ProxyError:
        print('requests.exceptions.ProxyError #', i)

    finally:
        return account_created


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

    my_args = parser.parse_args()
    number_of_threads = my_args.number_of_threads
    number_of_iterations = my_args.iters
    print_status_code = my_args.status_code
    delete_used_cookies = my_args.delete_used_cookies
    new_tech_data = my_args.new_tech_data
    infinite_iterations = True if number_of_iterations == -1 else False

    load_settings()

    number_of_iterations = load_data(number_of_iterations, delete_used_cookies)

    print_timeout = 10
    if number_of_threads >= 50:
        print_timeout *= 2.5
        if number_of_threads >= 100:
            print_timeout *= 2

    while True:
        for i in range(number_of_iterations):
            while len(threading.enumerate()) - 1 >= number_of_threads:
                time.sleep(0.001)

            th = threading.Thread(target=reg_account_wrapper, args=(i, print_status_code, new_tech_data))
            th.start()

            if i % print_timeout == 0:
                print('iters: ', i)
                print('threads: ', len(threading.enumerate())-1)

        if not infinite_iterations:
            break






