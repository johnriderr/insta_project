import requests
from settings_data import Cookie


# def get_cookie(proxy, u_agent):
#     """
#     :param session: requests session
#     :param proxy: '127:127:127:6666
#     :param u_agent: 'mozilla 123...
#     :return: from settings_data import Cookie
#     """
#     cookie_or_false = False
#     with requests.Session() as s:
#         headers = {
#             'User-Agent': u_agent,
#         }
#         r = s.get('https://www.instagram.com/', headers=headers, proxies={'http': 'http://{}:{}'.format(proxy.ip, proxy.port)})
#
#         if r.ok:
#             dt = s.cookies.get_dict()
#             try:
#                 cookie_or_false = Cookie(dt['csrftoken'], dt['rur'], dt['mid'], dt['ig_did'])
#             except KeyError:
#                 print('KeyError BAD: ', dt)
#             except AttributeError:
#                 print('AttributeError BAD: ', dt)
#             # print('GOOD: ', dt)
#
#     return cookie_or_false


def get_cookie(proxy, u_agent):
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
    r = requests.get('https://www.instagram.com/', headers=headers, proxies={'http': 'http://{}:{}'.format(proxy.ip, proxy.port)})

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
