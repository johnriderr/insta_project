import json, random, string
from network_classes import Proxy
from settings_data import settings_dict, SettingsData, Cookie
import os


def load_settings():
    if os.path.exists('resp_text.txt'):
        os.remove('resp_text.txt')

    with open('settings.txt') as f:
        settings_dict.update(json.load(f))
    settings_dict['gen_str_for_proxy'] = True if settings_dict['gen_str_for_proxy'] == 'yes' else False


def load_proxies(gen_str_for_proxy, count):
    with open(settings_dict['proxies_path']) as f:
        raw_proxies = [line.rstrip() for line in f.readlines()]

    proxies = []
    pr = raw_proxies[0]
    for i in range(count):
        tmp_pr = pr.split(':')
        if len(tmp_pr) == 4:  # proxy has ip, port, login, pass
            proxies.append(Proxy(tmp_pr[0], tmp_pr[1], tmp_pr[2], tmp_pr[3]))
        elif len(tmp_pr) == 2:  # proxy has ip and port
            proxies.append(Proxy(tmp_pr[0], tmp_pr[1], None, None))
        else:  # proxy parse error
            raise ValueError('Error data in proxy file')

    if gen_str_for_proxy:
        for pr in proxies:
            if pr.login:
                pr.login += '-session-{}'.format(
                    ''.join(random.choice(
                        string.ascii_uppercase + string.ascii_lowercase) for _ in range(random.randint(7, 10))))

    return proxies


def load_names(count):
    with open(settings_dict['names_path']) as f:
        names = [line.rstrip() for line in f.readlines()]
    while len(names) < count:
        names.append(names[random.randint(0, len(names)-1)])
    return names


def load_surnames(count):
    with open(settings_dict['surnames_path']) as f:
        surnames = [line.rstrip() for line in f.readlines()]
    while len(surnames) < count:
        surnames.append(surnames[random.randint(0, len(surnames)-1)])
    return surnames


def load_cookies(load_lines_count, delete_used=False):
    # Сколько строк прочли (load_lines) , столько удалили из файла
    cookies = []

    with open(settings_dict['cookies_path']) as f:
        # raw_cookies = [line.rstrip() for line in f.readlines()[:load_lines_count]]
        raw_cookies = [line.rstrip() for line in f.readlines()]
        if load_lines_count != -1:
            raw_cookies = raw_cookies[:load_lines_count]
    load_lines_count = len(raw_cookies)

    cookies = [Cookie(c.split(';')[0], c.split(';')[1], c.split(';')[2], c.split(';')[3]) for c in raw_cookies]
    if delete_used:
        with open(settings_dict['cookies_path'], 'r') as f:
            data = f.read().splitlines(True)
        with open(settings_dict['cookies_path'], 'w') as f:
            f.writelines(data[load_lines_count:])
    return cookies, load_lines_count


def load_locales():
    with open(settings_dict['locales_path']) as f:
        locales = [line.rstrip() for line in f.readlines()]
    return locales


def load_devices():
    with open(settings_dict['devices_path']) as f:
        devices = [line.rstrip() for line in f.readlines()]
    return devices


def load_data(number_of_iterations, delete_used_cookies):
    SettingsData.cookies, number_of_iterations = load_cookies(number_of_iterations, delete_used_cookies)

    SettingsData.proxies = load_proxies(settings_dict['gen_str_for_proxy'], number_of_iterations)
    SettingsData.names = load_names(number_of_iterations)
    SettingsData.surnames = load_surnames(number_of_iterations)
    SettingsData.locales = load_locales()
    SettingsData.devices = load_devices()
    return number_of_iterations