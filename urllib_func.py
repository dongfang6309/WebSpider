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


def get_header_info(path_header, path_userAgent=None, path_proxy=None):
    file_header = open(path_header, 'r')
    WebHeader: str = file_header.read()
    web_header = json.loads(WebHeader)
    file_header.close()
    if path_userAgent is not None:
        userAgent, userAgentLib = user_agent(path_userAgent)
        # web_header['User-Agent'] = userAgent
    if path_proxy is not None:
        userProxy, userProxyLib = user_proxy(path_proxy)
        proxy_handler = urllib.request.ProxyHandler(userProxy)
        # url_opener = urllib.request.build_opener(proxy_handler)
    http_handler = urllib.request.HTTPHandler()
    url_opener = urllib.request.build_opener(http_handler)
    return web_header, url_opener


class GetHtmlCode(object):
    def __init__(self, url, web_header, url_opener):
        self.url = url
        self.web_header = web_header
        self.url_opener = url_opener
        urllib.request.install_opener(self.url_opener)

    def get_method(self):
        # 进行get请求
        req = urllib.request.Request(self.url, headers=self.web_header)
        response = urllib.request.urlopen(req)
        html_code = response.read()
        return html_code

    def post_method(self, req_str, path_formData):
        file_formData = open(path_formData, 'r')
        FormData = file_formData.read()
        file_formData.close()
        form_data = json.loads(FormData)
        form_data['i'] = req_str
        data = urllib.parse.urlencode(form_data).encode(encoding='utf8')
        req = urllib.request.Request(self.url, data=data, headers=self.web_header)
        response = urllib.request.urlopen(req)
        html_code = response.read()
        return html_code


def write_html_code(html_code, path_phpFile):
    phpFile = open(path_phpFile, 'wb')
    phpFile.write(html_code)
    phpFile.close()
