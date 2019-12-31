import json, random, string, hashlib, requests, threading, time, sys
from load_settings_funcs import load_settings, load_data
from settings_data import SettingsData
import work_with_net as wwn


def reg_account_wrapper(i, print_status_code):
    next = 3
    try_reg = 0
    repeat_reg = False
    with requests.Session() as s:

        while True:
            # if try_reg > 0:
            #     repeat_reg = True
            if not reg_account(s, i, print_status_code, repeat_reg):
                break
            else:
                repeat_reg = True
                time.sleep(5)
            # try_reg += 1
            # if try_reg >= next:
            #     break


def reg_account(session, i, print_status_code, repeat):
    account_created = False
    user_agent = wwn.generate_user_agent(SettingsData.devices, SettingsData.locales)
    guid = wwn.generate_guid()
    guid2 = wwn.generate_guid()
    guid3 = wwn.generate_guid()
    adid = wwn.generate_guid()
    csrftoken = SettingsData.cookies[i].csrftoken
    # print(len(SettingsData.names))
    # time.sleep(10)
    mail = wwn.generate_mail(SettingsData.names[i])
    username = wwn.generate_username(mail)
    surname = SettingsData.surnames[i]
    device_id = wwn.generate_device_id()

    sn_nonce = wwn.generate_sn_nonce(mail)
    pw = wwn.generate_pw()

    data = wwn.generate_data(guid, guid2, guid3, adid, csrftoken, username, surname, device_id, mail, sn_nonce, pw)
    encrypted_data = wwn.encrypt_data_sha256(data)
    url_encoded_data = wwn.url_encode(data)

    # print('user_agent: {user_agent}\n'
    #       'csrftoken: {csrftoken}\n'
    #       'username: {username}\n'
    #       'device_id: {device_id}\n'
    #       'mail: {mail}\n'
    #       'sn_nonce: {sn_nonce}\n'
    #       'pw: {pw}\n'.format(
    #     user_agent=user_agent,
    #     csrftoken=csrftoken,
    #     username=username,
    #     device_id=device_id,
    #     mail=mail,
    #     sn_nonce=sn_nonce,
    #     pw=pw))
    try:
        resp = wwn.reg_request(user_agent, SettingsData.cookies[i], encrypted_data, url_encoded_data, session, SettingsData.proxies, i, repeat)
        if print_status_code:
            print('# {}. HTPP status code: {}'.format(i, resp.status_code))
        if 'created_user' in json.loads(resp.text):
            account_created = True
            if resp.ok:
                print('ok # {}'.format(i))
            # print(json.loads(resp.text))
            ds_user_id = json.loads(resp.text)['created_user']['pk']
            with open('goods.txt', 'a') as f:
                text_to_save = '{username}:{pw}-||{device_id};{guid2};{guid};{adid}|ds_user={username};' \
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
        # with open('resp_text.txt', 'a') as f:
        #     f.write('server output\n')
        #     f.write(resp.text)
        #     f.write('\n')
        #     f.write(str(session.cookies.get_dict()))
        #     f.write('\n\n')
    except requests.exceptions.ProxyError:
        print('requests.exceptions.ProxyError #', i)

    finally:
        return account_created


if __name__ == '__main__':
    print_status_code = False
    delete_used_cookies = False
    if len(sys.argv) >= 3:
        number_of_threads, number_of_iterations = sys.argv[1:3]
        number_of_threads = int(number_of_threads)
        number_of_iterations = int(number_of_iterations)
        if len(sys.argv) >= 4:
            for arg in sys.argv:
                if arg =='/O':
                    print_status_code = True
                if arg == '/D':
                    delete_used_cookies = True

    else:
        print('main.py M N [/O] [/D]')
        print('M - threads, N - iterations, /O - необязательный ключ Output status code, /D - необязательный ключ'
              'для удаления использованных куки из файла')
        sys.exit()
    # number_of_threads = 5
    # number_of_iterations = 300

    load_settings()

    load_data(number_of_iterations, delete_used_cookies)

    # SettingsData.mails = wwn.generate_mails(SettingsData.names, number_of_iterations)

    # SettingsData.usernames = wwn.generate_usernames(SettingsData.mails)

    print_timeout = 10
    if number_of_threads >= 50:
        print_timeout *= 2.5
        if number_of_threads >= 100:
            print_timeout *= 2
    # if print_status_code:
    #     print_timeout = 1

    for i in range(number_of_iterations):
        while len(threading.enumerate()) - 1 >= number_of_threads:
            time.sleep(0.001)

        th = threading.Thread(target=reg_account_wrapper, args=(i, print_status_code,))
        th.start()

        if i % print_timeout == 0:
            print('iters: ', i)
            print('threads: ', len(threading.enumerate())-1)








