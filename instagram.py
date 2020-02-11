import requests, hashlib, urllib, time, base64, json, threading, os
from random import randint, choice
import string


class Cookie:
    def __init__(self, csrftoken, rur, mid, ajax):
        self.csrftoken = csrftoken
        self.rur = rur
        self.mid = mid

    def __str__(self):
        return 'csrftoken:{} rur:{} mid:{}'.format(self.csrftoken, self.rur, self.mid)


class Proxy:
    def __init__(self, ip, port, login=None, pw=None):
        self.ip = ip
        self.port = port
        self.login = login
        self.pw = pw

    def __str__(self):
        return 'IP: {}, Port: {}, Login: {}, Pass: {}'.format(self.ip, self.port, self.login, self.pw)


class Instagram(threading.Thread):
    def __init__(self, args, settings, proxy, cookie, user_agent, name, surname, device, locale, thr_id=None):
        threading.Thread.__init__(self)
        self.session = requests.session()
        self.settings = settings
        gen_str = ''
        if args['gen_str_for_proxy']:
            gen_str = self.gen_str_for_proxy_to_add_to_login()
        my_proxy = {
            "https": "http://{}:{}@{}:{}".format(proxy.login + gen_str, proxy.pw, proxy.ip, proxy.port)
        }
        self.session.proxies.update(my_proxy)
        self.proxy = proxy
        self.cookie = cookie
        self.user_agent = user_agent
        self.name = name
        self.surname = surname
        self.device = device
        self.locale = locale
        self.mail = self.generate_mail(self.name)
        self.username = self.generate_username(self.name)
        self.args = args
        self.guid = self.generate_guid()
        self.guid2 = self.generate_guid()
        self.guid3 = self.generate_guid()
        self.adid = self.generate_guid()

        lock = threading.Lock()
        lock.acquire()

        if self.args['device_id_from_file']:
            len_line = len('android-twday94lnom8i9t3')+2
            with open(settings['devices_id_path'], 'rb+') as f:
                f.seek(-len_line, os.SEEK_END)
                self.device_id = f.read(len_line).decode("utf-8").strip()
                f.seek(-len_line, os.SEEK_END)
                f.truncate()
        else:
            self.device_id = self.generate_device_id()
        if self.device_id.find('android') == -1:
            print('Проверьте файл ' + settings['devices_id_path'])
            import sys
            sys.exit()
        lock.release()

        self.thr_id = thr_id

        self.encrypted_data = None

    def create_account(self):
        account_created = False
        repeat_reg = False
        headers = {'User-Agent': self.user_agent, 'X-IG-Connection-Speed': str(randint(1, 3000)) + 'kbps',
                   'X-IG-Bandwidth-Speed-KBPS': '{}.{}'.format(randint(1, 3000), randint(100, 300)),
                   'X-IG-Bandwidth-TotalBytes-B': str(randint(100, 9999)),
                   'X-IG-Bandwidth-TotalTime-MS': str(randint(50, 500)),
                   'X-IG-Connection-Type': 'WIFI',
                   'X-IG-Capabilities': '3brTvw==',
                   'X-IG-App-ID': '567067343352427',
                   'Accept-Language': 'fr_FR',
                   'Cookie': 'mid={0}; csrftoken={1}; rur={2}'.format(self.cookie.mid, self.cookie.csrftoken, self.cookie.rur),
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Host': 'i.instagram.com',
                   'Connection': 'Keep-Alive',
                   'Accept-Encoding': 'gzip'
                   }
        # mail = self.generate_mail(self.name)
        # username = self.generate_username(mail)
        sn_nonce = self.generate_sn_nonce(self.mail)
        pw = self.generate_pw()
        data = self.generate_data_for_create_account(self.guid, self.guid2, self.guid3, self.adid, self.cookie.csrftoken,
                                                     self.username, self.surname, self.device_id, self.mail, sn_nonce, pw)
        # print('data to send:')
        # print(data)
        encrypted_data = self.encrypt_data_sha256(data)
        self.encrypted_data = encrypted_data

        url_encoded_data = self.url_encode(data)
        body = 'signed_body={0}.{1}&ig_sig_key_version=4'.format(encrypted_data, url_encoded_data)
        try:
            r = self.session.post('https://i.instagram.com/api/v1/accounts/create/', data=body, headers=headers)
            # print(json.loads(r.text))
            # print('-'*200)
            if self.args['print_status_code']:
                print('# {}. HTPP status code: {}'.format(self.thr_id, r.status_code))
            if 'created_user' in json.loads(r.text):
                if r.ok:
                    account_created = True
                    print('ok # {}'.format(self.thr_id))
                    # print('ok - {}'.format(username))
                    import winsound
                    winsound.Beep(300, 100)

                    ds_user_id = json.loads(r.text)['created_user']['pk']
                    session_id = self.session.cookies.get_dict()['sessionid']

                    with open('goods.txt', 'a') as f:
                        u_agent_to_save = self.user_agent if self.args['save_with_user_agent'] else ''
                        text_to_save = '{username}:{pw}|{u_agent_to_save}|{device_id};{guid2};{guid};{adid}|ds_user={username};' \
                                       'rur={rur};mid={mid};csrftoken={csrftoken};ds_user_id={ds_user_id};' \
                                       'sessionid={session_id};is_starred_enabled=yes;urlgen=;||'.format(
                                                                username=username, pw=pw,
                                                                device_id=self.device_id,
                                                                guid2=self.guid2, guid=self.guid, adid=self.adid,
                                                                rur=self.cookie.rur,
                                                                mid=self.cookie.mid,
                                                                csrftoken=self.cookie.csrftoken,
                                                                ds_user_id=ds_user_id,
                                                                session_id=session_id,
                                                                u_agent_to_save=u_agent_to_save)

                        f.write(text_to_save)
                        f.write('\n')
                    if self.args['save_in_json']:
                        with open('goods_json.txt', 'a') as f:


                                # dict_to_save = {'username': username, 'pw': pw, 'user_agent': self.user_agent, device_id=self.device_id}
                                dict_to_save = dict(username=username, pw=pw,
                                                    device_id=self.device_id,
                                                    guid2=self.guid2,
                                                    guid=self.guid,
                                                    adid=self.adid,
                                                    guid3=self.guid3,
                                                    rur=self.cookie.rur,
                                                    mid=self.cookie.mid,
                                                    csrftoken=self.cookie.csrftoken,
                                                    ds_user_id=ds_user_id,
                                                    session_id=session_id,
                                                    user_agent=self.user_agent,
                                                    surname=self.surname,
                                                    sn_nonce=sn_nonce)
                                f.write(str(dict_to_save))
                                f.write('\n')
                    if self.args['set_bio']:
                        with open(self.settings['biography'], 'r') as f:
                            bio_text = f.read()

                        self.set_bio(self.session.cookies.get_dict()['sessionid'], ds_user_id, bio_text)
                    if self.args['subscribe']:
                        insta_users_id = []
                        with open(self.settings['subscribe_path'], 'r') as f:
                            insta_users_id = [line.strip() for line in f.readlines()]
                        for u_id in insta_users_id:
                            print('id to subs: {}'.format(u_id))
                            self.subscribe(session_id, ds_user_id, u_id)

        except requests.exceptions.ProxyError:
            print('requests.exceptions.ProxyError #', self.thr_id)
        except Exception as e:
            print('another exception #', self.thr_id,  str(e))

        return account_created

    def subscribe(self, session_id, user_id, user_id_to_subscribe):
        headers = {'User-Agent': self.user_agent, 'X-IG-Connection-Speed': str(randint(1, 3000)) + 'kbps',
                   'X-IG-Bandwidth-Speed-KBPS': '{}.{}'.format(randint(1, 3000), randint(100, 300)),
                   'X-IG-Bandwidth-TotalBytes-B': str(randint(100, 9999)),
                   'X-IG-Bandwidth-TotalTime-MS': str(randint(50, 500)),
                   'X-IG-Connection-Type': 'WIFI',
                   'X-IG-Capabilities': '3brTvw==',
                   'X-IG-App-ID': '567067343352427',
                   'Accept-Language': 'fr_FR',
                   'Cookie': 'sessionid={3}; mid={0}; csrftoken={1}; rur={2}'.format(self.cookie.mid,
                                                                                     self.cookie.csrftoken,
                                                                                     self.cookie.rur, session_id),
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Host': 'i.instagram.com',
                   'Connection': 'Keep-Alive',
                   'Accept-Encoding': 'gzip'}

        data = self.gen_data_for_subscribe()
        encrypted_data = self.encrypt_data_sha256(data)
        body = 'signed_body={}.{}&ig_sig_key_version=4'.format(encrypted_data, data)

        r = requests.post('https://i.instagram.com/api/v1/friendships/create/393066635/', data=body, headers=headers)

    def set_bio(self, session_id, user_id, bio_text):
        headers = {'User-Agent': self.user_agent, 'X-IG-Connection-Speed': str(randint(1, 3000)) + 'kbps',
                   'X-IG-Bandwidth-Speed-KBPS': '{}.{}'.format(randint(1, 3000), randint(100, 300)),
                   'X-IG-Bandwidth-TotalBytes-B': str(randint(100, 9999)),
                   'X-IG-Bandwidth-TotalTime-MS': str(randint(50, 500)),
                   'X-IG-Connection-Type': 'WIFI',
                   'X-IG-Capabilities': '3brTvw==',
                   'X-IG-App-ID': '567067343352427',
                   'Accept-Language': 'fr_FR',
                   'Cookie': 'sessionid={3}; mid={0}; csrftoken={1}; rur={2}'.format(self.cookie.mid,
                                                                                     self.cookie.csrftoken,
                                                                                     self.cookie.rur, session_id),
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Host': 'i.instagram.com',
                   'Connection': 'Keep-Alive',
                   'Accept-Encoding': 'gzip'}

        data = self.gen_data_for_change_bio(self.cookie.csrftoken, user_id, self.device_id, bio_text)
        encrypted_data = self.encrypt_data_sha256(data)
        body = 'signed_body={}.{}&ig_sig_key_version=4'.format(encrypted_data, data)

        r = requests.post('https://i.instagram.com/api/v1/accounts/set_biography/', data=body, headers=headers)

    def gen_data_for_subscribe(self, user_id, user_id_to_subscribe):
        data = '{{"_csrftoken":"{csrftoken}","user_id":"{user_id_to_subscribe}","radio_type":"wifi-none",' \
               '"_uid":"{user_id}","device_id":"android-2503eaab5a2d6349","_uuid":"{guid}"}}'
        guid = self.generate_guid()
        data = data.format(csrftoken=self.cookie.csrftoken, uid=user_id,
                           device_id=self.device_id, user_id_to_subscribe=user_id_to_subscribe, guid=guid)

        return data

    def gen_data_for_change_bio(self, csrftoken, user_id, device_id, text):
        data = '{{"_csrftoken":"{csrftoken}","_uid":"{user_id}","device_id":"{device_id}",' \
               '"_uuid":"{guid}","raw_text":"{text}"}}'

        guid = self.generate_guid()
        data = data.format(csrftoken=csrftoken, user_id=user_id,
                           device_id=device_id, text=text, guid=guid)
        print(data)
        return data

    def run(self):
        while True:
            if not self.create_account():
                break

    @staticmethod
    def gen_str_for_proxy_to_add_to_login():
        return '-session-{}'.format(
            ''.join(choice(
                string.ascii_uppercase + string.ascii_lowercase) for _ in range(randint(7, 10))))

    @staticmethod
    def generate_pw():
        return ''.join([choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
                        for _ in range(randint(8, 10))])

    @staticmethod
    def generate_sn_nonce(mail):
        timestamp = int(time.time())
        rand_str = ''.join([choice(string.ascii_lowercase + string.digits) for _ in range(randint(12, 12))])
        tobase64 = '{0}|{1}|{2}'.format(mail, timestamp, rand_str)
        b64_encoded = base64.b64encode(tobase64.encode()).decode("utf-8")
        return b64_encoded

    @staticmethod
    def generate_mail(name):
        mail = '{0}.{1}_{2}@gmail.com'.format(
            name,
            ''.join([choice(string.ascii_lowercase) for _ in range(9)]),
            randint(10000, 100000)
        )
        return mail

    @staticmethod
    def generate_username(name):
        username = '{}{}{}'.format(
            name,
            ''.join([choice(string.ascii_lowercase) for _ in range(7, 10)]),
            randint(100, 999999))
        return username

    @staticmethod
    def generate_guid():
        # d167b6ad-0082-4458-872d-e8de1eefd328
        rstr = lambda length: ''.join([choice(string.ascii_lowercase + string.digits)
                                       for _ in range(randint(length, length))])
        return '{0}-{1}-{2}-{3}'.format(rstr(8), rstr(4), rstr(4), rstr(12))

    @staticmethod
    def generate_device_id():
        # android-2bmg4rhe192d0f03
        return 'android-' + ''.join([choice(string.ascii_lowercase + string.digits)
                                     for _ in range(randint(16, 16))])

    @staticmethod
    def generate_data_for_create_account(guid, guid2, guid3, adid, csrftoken, username, surname, device_id, mail, sn_nonce, pw):
        data = '{{"tos_version":"row","suggestedUsername":"","allow_contacts_sync":"true","sn_result":"API_ERROR:+null",' \
               '"phone_id":"{guid2}","_csrftoken":"{csrftoken}","username":"{username}",' \
               '"first_name":"{surname}","adid":"{adid}","guid":"{guid}",' \
               '"device_id":"{device_id}","email":"{mail}","sn_nonce":"{sn_nonce}",' \
               '"force_sign_up_code":"","waterfall_id":"{guid3}","qs_stamp":"","password":"{pw}"}}'
        data = data.format(guid2=guid2, csrftoken=csrftoken, username=username, surname=surname, adid=adid,
                           guid=guid, device_id=device_id, mail=mail, sn_nonce=sn_nonce, guid3=guid3, pw=pw)
        return data

    @staticmethod
    def encrypt_data_sha256(data):
        m = hashlib.sha256()
        m.update(data.encode())
        return m.hexdigest()

    @staticmethod
    def url_encode(data):
        return urllib.parse.quote(data)

    @staticmethod
    def generate_user_agent(settings, devices, locales):
        rand_locale = locales[randint(0, len(locales) - 1)]
        rand_device = devices[randint(0, len(devices) - 1)]
        rand_device = '  '.join(rand_device.split()[:-2])
        user_agent = 'Instagram {0} Android ({1} {2}; {3})'.format(
            settings['version'],
            rand_device,
            rand_locale,
            settings['version_code']
        )
        return user_agent

    @staticmethod
    def get_cookie_from_request(proxy, u_agent):
        """
        :param session: requests session
        :param proxy: '127:127:127:6666
        :param u_agent: 'mozilla 123...
        :return: from settings_data import Cookie
        """
        cookie_or_false = False
        # with requests.Session() as s:
        headers = {
            'User-Agent': u_agent,
        }
        # r = s.get('http://www.showmemyip.com/',  proxies={'http': 'http://{}:{}'.format(proxy.ip, proxy.port)})
        # print('get cokie: ', r.text)
        r = requests.get('https://www.instagram.com/', headers=headers,
                         proxies={'http': 'http://{}:{}'.format(proxy.ip, proxy.port)})

        if r.ok:
            dt = r.cookies.get_dict()
            try:
                cookie_or_false = Cookie(dt['csrftoken'], dt['rur'], dt['mid'], dt['ig_did'])
            except KeyError:
                print('KeyError BAD: ', dt)
            except AttributeError:
                print('AttributeError BAD: ', dt)
            # print('GOOD: ', dt)
        return cookie_or_false
