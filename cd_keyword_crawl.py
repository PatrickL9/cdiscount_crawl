# -*- coding: UTF-8 -*-
#!/usr/bin/python3

"""
cdiscount平台根据关键词搜索，查询前3页查询结果的详情页信息
@Author ：Patrick Lam
@Date ：2023-02-13
"""
import os
import random
import time
import requests
from lxml import etree
from util import logging_util
from util.setting import logging, ipPool, headers, PROXY_URL


def get_ip_pool():
    """
    获取IP代理池
    :param
    :return:
    """
    logging.info('获取IP代理，搭建代理IP池')
    ips = requests.get(PROXY_URL)
    for ip in ips.text.split('\r\n'):
        if len(ip) > 8:
            ipPool.append('http://' + ip)


def get_random_ip():
    """
    获取随机代理IP
    :param
    :return:随机代理IP
    """
    ip = random.choice(ipPool)
    logging.info('获取随机代理IP: ' + ip)
    return ip


def get_all_url(url_r):
    """
    爬取初始url页面中所有的产品url
    :param url_r: 初始url
    :return:product_list: 所有产品url
    """
    product_list = []
    # proxies = {'http': get_random_ip()}
    resp = requests.get(url_r, headers=headers, timeout=30)
    text = resp.content.decode('utf-8')
    html = etree.HTML(text)
    print(text)

if __name__ == '__main__':
    crawl_url = 'https://www.cdiscount.com/search/10/poussette+double.html#_his_'
    test_url = 'https://www.cdiscount.com/pret-a-porter/bebe-puericulture/hauck-poussette-jumeaux-roadster-duo-slx-gris-si/f-113173501-hau4007923512173.html?idOffre=2195544923#mpos=0|mp'
    get_ip_pool()
    get_all_url(test_url)



