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


class SettingsDataClass:
    def __init__(self):
        self.proxies = None
        self.names = None
        self.surnames = None
        self.cookies = None
        self.devices = None
        self.locales = None
        # self.mails = None
        # self.usernames = None


SettingsData = None
if SettingsData is None:
    SettingsData = SettingsDataClass()
