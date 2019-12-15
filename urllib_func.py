# coding=UTF-8<code>
import urllib.request
import urllib.parse
import re
import json
import random


def user_agent(path_userAgent):
    file_userAgent = open(path_userAgent, 'r')
    userAgentLib = []
    for line in file_userAgent.readlines():
        line = line.strip()
        userAgentLib.append(line)
    file_userAgent.close()
    userAgent = random.choice(userAgentLib)
    return userAgent, userAgentLib


def user_proxy(path_proxy):
    file_proxy = open(path_proxy)
    userProxyLib = file_proxy.read()
    file_proxy.close()
    userProxyLib = json.loads(userProxyLib)
    userProxy = random.choice(userProxyLib)
    return userProxy, userProxyLib


def get_header_info(path_header, path_userAgent, path_proxy):
    userAgent, userAgentLib = user_agent(path_userAgent)
    userProxy, userProxyLib = user_proxy(path_proxy)
    file_header = open(path_header, 'r')
    WebHeader: str = file_header.read()
    web_header = json.loads(WebHeader)
    file_header.close()
    # web_header['User-Agent'] = userAgent

    proxy_handler = urllib.request.ProxyHandler(userProxy)
    http_handler = urllib.request.HTTPHandler()
    url_opener = urllib.request.build_opener(http_handler)
    return web_header, url_opener


def get_html_code(url, web_header, url_opener):
    urllib.request.install_opener(url_opener)

    # 进行get请求
    req = urllib.request.Request(url, headers=web_header)
    response = urllib.request.urlopen(req)
    html_code = response.read()
    return html_code


def write_html_code(html_code, path_phpFile):
    phpFile = open(path_phpFile, 'wb')
    phpFile.write(html_code)
    phpFile.close()
