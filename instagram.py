import requests, hashlib, urllib
from random import randint


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


class Instagram:
    def __init__(self, settings, args, proxy, cookie, user_agent):
        self.session = requests.session()
        my_proxy = {
            "https": "http://{}:{}@{}:{}".format(proxy.login, proxy.pw, proxy.ip, proxy.port)
        }
        self.session.proxies.update(my_proxy)
        self.proxy = proxy
        self.cookie = cookie
        self.user_agent = user_agent

    def create_account(self):
        headers = {'User-Agent': self.user_agent, 'X-IG-Connection-Speed': str(randint(1, 3000)) + 'kbps',
                   'X-IG-Bandwidth-Speed-KBPS': '{}.{}'.format(randint(1, 3000), randint(100, 300)),
                   'X-IG-Bandwidth-TotalBytes-B': str(randint(100, 9999)),
                   'X-IG-Bandwidth-TotalTime-MS': str(randint(50, 500)),
                   'X-IG-Connection-Type': 'WIFI',
                   'X-IG-Capabilities': '3brTvw==',
                   'X-IG-App-ID': '567067343352427',
                   'Accept-Language': 'fr_FR',
                   'Cookie': 'mid={0}; csrftoken={1}; rur={2}'.format(self.cookies.mid, self.cookies.csrftoken, self.cookies.rur),
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Host': 'i.instagram.com',
                   'Connection': 'Keep-Alive',
                   'Accept-Encoding': 'gzip'
                   }

        data = self.generate_data(guid, guid2, guid3, adid, cookie.csrftoken, username, surname, device_id, mail,
                                 sn_nonce, pw)

        encrypted_data = self.encrypt_data_sha256(data)
        url_encoded_data = self.url_encode(data)

        body = 'signed_body={0}.{1}&ig_sig_key_version=4'.format(encrypted_data, url_encoded_data)
        r = self.session.post('https://i.instagram.com/api/v1/accounts/create/', data=body, headers=headers)
        return r

    def generate_data(self, guid, guid2, guid3, adid, csrftoken, username, surname, device_id, mail, sn_nonce, pw):
        data = '{{"tos_version":"row","suggestedUsername":"","allow_contacts_sync":"true","sn_result":"API_ERROR:+null",' \
               '"phone_id":"{guid2}","_csrftoken":"{csrftoken}","username":"{username}",' \
               '"first_name":"{surname}","adid":"{adid}","guid":"{guid}",' \
               '"device_id":"{device_id}","email":"{mail}","sn_nonce":"{sn_nonce}",' \
               '"force_sign_up_code":"","waterfall_id":"{guid3}","qs_stamp":"","password":"{pw}"}}'
        data = data.format(guid2=guid2, csrftoken=csrftoken, username=username, surname=surname, adid=adid,
                           guid=guid, device_id=device_id, mail=mail, sn_nonce=sn_nonce, guid3=guid3, pw=pw)
        return data

    def encrypt_data_sha256(self, data):
        m = hashlib.sha256()
        m.update(data.encode())
        return m.hexdigest()

    def url_encode(self, data):
        return urllib.parse.quote(data)