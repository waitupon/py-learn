#!/bin/env/python
# *_*coding:utf-8 *_*

from pycookiecheat import chrome_cookies
import requests
# import pycookiecheat



if __name__ == '__main__':
    url = 'http://baidu.com/'

    # Uses Chrome's default cookies filepath by default
    cookies = chrome_cookies(url)
    print(cookies)
    r = requests.get(url, cookies=cookies)
    print(r.text)

    pass