import random, string, time, base64, hashlib, json, requests
from random import randint
from settings_data import settings_dict
import urllib.parse


def generate_mails(names, count):
    mails = []
    i = 0
    while len(mails) < count:
        mail = generate_mail(names[i])
        mails.append(mail)
        i += 1
        if i == len(names):
            i = 0
    return mails


def generate_mail(name):
    mail = '{0}.{1}_{2}@gmail.com'.format(
        name,
        ''.join([random.choice(string.ascii_lowercase) for _ in range(9)]),
        randint(10000, 100000))
    return mail


def generate_usernames(mails):
    usernames =[]
    for mail in mails:
        usernames.append(generate_username(mail))
    return usernames


def generate_username(mail):
    return mail.split('@')[0]


def generate_user_agent(devices, locales):
    rand_locale = locales[randint(0, len(locales)-1)]
    rand_device = devices[randint(0, len(devices)-1)]
    rand_device = '  '.join(rand_device.split()[:-2])
    user_agent = 'Instagram {0} Android ({1} {2}; {3})'.format(
        settings_dict['version'],
        rand_device,
        rand_locale,
        settings_dict['version_code']
    )
    return user_agent


def generate_pw():
    return ''.join([random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
                    for _ in range(randint(8, 10))])


def generate_device_id():
    # android-2bmg4rhe192d0f03
    return 'android-' + ''.join([random.choice(string.ascii_lowercase + string.digits)
                               for _ in range(randint(16, 16))])


def generate_guid():
    # d167b6ad-0082-4458-872d-e8de1eefd328
    rstr = lambda length: ''.join([random.choice(string.ascii_lowercase + string.digits)
                               for _ in range(randint(length, length))])
    return '{0}-{1}-{2}-{3}'.format(rstr(8), rstr(4), rstr(4), rstr(12))


def generate_sn_nonce(mail):
    timestamp = int(time.time())
    rand_str = ''.join([random.choice(string.ascii_lowercase + string.digits) for _ in range(randint(12, 12))])
    tobase64 = '{0}|{1}|{2}'.format(mail, timestamp, rand_str)
    b64_encoded = base64.b64encode(tobase64.encode()).decode("utf-8")
    return b64_encoded


def generate_data(guid, guid2, guid3, adid,  csrftoken, username, surname, device_id, mail, sn_nonce, pw):
    data = '{{"tos_version":"row","suggestedUsername":"","allow_contacts_sync":"true","sn_result":"API_ERROR:+null",' \
           '"phone_id":"{guid2}","_csrftoken":"{csrftoken}","username":"{username}",' \
           '"first_name":"{surname}","adid":"{adid}","guid":"{guid}",' \
           '"device_id":"{device_id}","email":"{mail}","sn_nonce":"{sn_nonce}",' \
           '"force_sign_up_code":"","waterfall_id":"{guid3}","qs_stamp":"","password":"{pw}"}}'
    data = data.format(guid2=guid2, csrftoken=csrftoken, username=username, surname=surname, adid=adid,
                       guid=guid, device_id=device_id, mail=mail, sn_nonce=sn_nonce, guid3=guid3, pw=pw)
    return data


def encrypt_data_sha256(data):
    m = hashlib.sha256()
    m.update(data.encode())
    return m.hexdigest()


def url_encode(data):
    # data = {'q': 'Python URL encoding', 'as_sitesearch': 'www.urlencoder.io'}
    # print('data')
    # print(data)
    # print()
    # print('urllib.parse.urlencode(json.loads(data))')
    # print(urllib.parse.urlencode(json.loads(data)))
    # print()
    # print('urllib.parse.quote(data)')
    # print(urllib.parse.quote(data))
    # print()

    return urllib.parse.quote(data)


def reg_request(user_agent, cookie, encrypted_data, url_encoded_data, session, proxies, i, repeat):
    headers = {'User-Agent': user_agent, 'X-IG-Connection-Speed': str(randint(1, 3000)) + 'kbps',
               'X-IG-Bandwidth-Speed-KBPS': '{}.{}'.format(randint(1, 3000), randint(100, 300)),
               'X-IG-Bandwidth-TotalBytes-B': str(randint(100, 9999)),
               'X-IG-Bandwidth-TotalTime-MS': str(randint(50, 500)),
               'X-IG-Connection-Type': 'WIFI',
               'X-IG-Capabilities': '3brTvw==',
               'X-IG-App-ID': '567067343352427',
               'Accept-Language': 'fr_FR',
               'Cookie': 'mid={0}; csrftoken={1}; rur={2}'.format(cookie.mid, cookie.csrftoken, cookie.rur),
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Host': 'i.instagram.com',
               'Connection': 'Keep-Alive',
               'Accept-Encoding': 'gzip'
               }
    body = 'signed_body={0}.{1}&ig_sig_key_version=4'.format(encrypted_data, url_encoded_data)
    # print(encrypted_data)
    # print(url_encoded_data)
    # print(body)
    # body='signed_body=e1134a48d7aa748c81d95481ff1baa60fd5dd3a5d2fa3e2ec37ac96b137c2551.%7b%22tos_version%22%3a%22row%22%2c%22suggestedUsername%22%3a%22%22%2c%22allow_contacts_sync%22%3a%22true%22%2c%22sn_result%22%3a%22API_ERROR%3a%2bnull%22%2c%22phone_id%22%3a%22ffafebac-ff11-40a2-acb1-ffec6c7451dd%22%2c%22_csrftoken%22%3a%22rlunUuWJkhpNwO6gqHchpihdTXQgZQhr%22%2c%22username%22%3a%22Nova.loxqxtn_21867%22%2c%22first_name%22%3a%22vil%22%2c%22adid%22%3a%22f97ef285-6fb1-4f42-a2a8-315f8967ccdc%22%2c%22guid%22%3a%22a8574181-dd16-447e-a9a4-1a4222860603%22%2c%22device_id%22%3a%22android-h24w495xyq5wjwm3%22%2c%22email%22%3a%22Nova.loxqxtn_21867%40gmail.com%22%2c%22sn_nonce%22%3a%22Tm92YS5sb3hxeHRuXzIxODY3QGdtYWlsLmNvbXwxNTc3MjQ2NzYyfGtxNmNVSHd6VkVjWQ%3d%3d%22%2c%22force_sign_up_code%22%3a%22%22%2c%22waterfall_id%22%3a%22fd30b6de-6237-4921-af07-674979778d8d%22%2c%22qs_stamp%22%3a%22%22%2c%22password%22%3a%22oKnZXwcU1%22%7d&ig_sig_key_version=4'

    # pr_login = 'lum-customer-aklimkin-zone-zone3test'
    # pr_login += '-session-{}'.format(
    #     ''.join(random.choice(
    #         string.ascii_uppercase + string.ascii_lowercase) for _ in range(random.randint(7, 10))))
    # print(proxy)

    mproxies = {
        "https": "http://{}:{}@{}:{}".format(proxies[i].login, proxies[i].pw,  proxies[i].ip, proxies[i].port)
    }
    if not repeat:
        session.proxies.update(mproxies)
    # r = session.post('https://jsonip.com/')
    # print(r.json()['ip'], r.status_code)
    # with open('ip.txt', 'a') as f:
    #     f.write('{}\n'.format( r.json()['ip']))
    # print('BODY:')
    # print(body)
    # print('headers:')
    # print(headers)

    # with open('resp_text.txt', 'a') as f:
    #     f.write('BODY:\n')
    #     f.write(body)
    #     f.write('\n')
    #     f.write('headers:\n')
    #     f.write(str(headers))
    #     f.write('\n')

    r = session.post('https://i.instagram.com/api/v1/accounts/create/', data=body, headers=headers, proxies=mproxies)
    return r
