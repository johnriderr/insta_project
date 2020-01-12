settings_dict = None
if settings_dict is None:
    settings_dict = {}


# from collections import namedtuple
# Cookie = namedtuple('Cookie', 'csrftoken rur mid ajax')


class Cookie:
    def __init__(self, csrftoken, rur, mid, ajax):
        self.csrftoken = csrftoken
        self.rur = rur
        self.mid = mid
        self.ajax = ajax

    def __str__(self):
        return 'csrftoken:{} rur:{} mid:{} ajax:{}'.format(self.csrftoken, self.rur, self.mid, self.ajax)


class SettingsDataClass:
    def __init__(self):
        self.proxies = None
        self.names = None
        self.surnames = None
        self.cookies = None
        self.devices = None
        self.locales = None
        self.user_agents_for_getting_cookies = None
        self.proxies_for_getting_cookies = None
        self.gen_str_for_proxy = None
        # self.mails = None
        # self.usernames = None


SettingsData = None
if SettingsData is None:
    SettingsData = SettingsDataClass()
