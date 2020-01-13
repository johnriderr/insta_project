import json, random, string
from network_classes import Proxy
from settings_data import SettingsData, Cookie
import os


def load_settings():
    with open('settings.txt') as f:
        settings = json.load(f)
        settings['gen_str_for_proxy'] = bool(settings['gen_str_for_proxy'])
    return settings


def load_proxies(settings):
    with open(settings['proxies_path']) as f:
        raw_proxies = [line.rstrip() for line in f.readlines()]

    proxies = []
    ip = raw_proxies[0].split(':')[0]
    port = raw_proxies[0].split(':')[1]
    login = raw_proxies[0].split(':')[2]
    pw = raw_proxies[0].split(':')[3]
    proxies.append(Proxy(ip, port, login, pw))
    #
    #
    # if gen_str_for_proxy:
    #     for pr in proxies:
    #         if pr.login:
    #             pr.login += '-session-{}'.format(
    #                 ''.join(random.choice(
    #                     string.ascii_uppercase + string.ascii_lowercase) for _ in range(random.randint(7, 10))))

    return proxies


def load_names(settings):
    with open(settings['names_path']) as f:
        names = [line.rstrip() for line in f.readlines()]
    return names


def load_surnames(settings):
    with open(settings['surnames_path']) as f:
        surnames = [line.rstrip() for line in f.readlines()]
    return surnames


def load_cookies(settings, load_lines_count, delete_used=False):
    # Сколько строк прочли (load_lines) , столько удалили из файла
    cookies = []

    with open(settings['cookies_path']) as f:
        # raw_cookies = [line.rstrip() for line in f.readlines()[:load_lines_count]]
        raw_cookies = [line.rstrip() for line in f.readlines()]
        if load_lines_count != -1:
            raw_cookies = raw_cookies[:load_lines_count]
    load_lines_count = len(raw_cookies)

    cookies = [Cookie(c.split(';')[0], c.split(';')[1], c.split(';')[2], c.split(';')[3]) for c in raw_cookies]
    if delete_used:
        with open(settings['cookies_path'], 'r') as f:
            data = f.read().splitlines(True)
        with open(settings['cookies_path'], 'w') as f:
            f.writelines(data[load_lines_count:])
    return cookies, load_lines_count


def load_locales(settings):
    with open(settings['locales_path']) as f:
        locales = [line.rstrip() for line in f.readlines()]
    return locales


def load_devices(settings):
    with open(settings['devices_path']) as f:
        devices = [line.rstrip() for line in f.readlines()]
    return devices


def load_data(settings, number_of_iterations, delete_used_cookies, cookie_from_request):
    if not cookie_from_request:
        SettingsData.cookies, number_of_iterations = load_cookies(settings, number_of_iterations, delete_used_cookies)

    SettingsData.proxies = load_proxies(settings)
    SettingsData.names = load_names(settings)
    SettingsData.surnames = load_surnames(settings)
    SettingsData.locales = load_locales(settings)
    SettingsData.devices = load_devices(settings)
    return number_of_iterations


def load_user_agents_for_getting_cookies(settings):
    with open(settings['user_agents_for_getting_cookies']) as f:
        user_agents = [line.rstrip() for line in f.readlines()]
    SettingsData.user_agents_for_getting_cookies = user_agents


def load_proxies_for_getting_cookies(settings):
    with open(settings['proxies_for_getting_cookies']) as f:
        proxies = [line.rstrip() for line in f.readlines()]
    SettingsData.proxies_for_getting_cookies = proxies