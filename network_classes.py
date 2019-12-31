class Proxy:
    def __init__(self, ip, port, login=None, pw=None):
        self.ip = ip
        self.port = port
        self.login = login
        self.pw = pw

    def __str__(self):
        return 'IP: {}, Port: {}, Login: {}, Pass: {}'.format(self.ip, self.port, self.login, self.pw)

