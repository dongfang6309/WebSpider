# coding=UTF-8<code>
import urllib.request
import urllib.parse
import re
import json
import random
import time
import hashlib


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


def read_txt2json(path_txt):
    file_txt = open(path_txt, 'rb')
    txt_trans = '{'
    for each in file_txt.readlines():
        each = each.decode()
        if each.find('[') and each.find(']') is not -1:
            each = each[0:len(each) - 2]
        else:
            each = '\"' + each
            ls_each = list(each)
            ls_each.remove(' ')
            ls_each.insert(each.find(':'), '\"')
            each = ''.join(ls_each)
            ls_each = list(each)
            ls_each.insert(each.find(':') + 1, '\"')
            each = ''.join(ls_each)
            each = each[0:len(each) - 2]
            # 'rb'读取文件时，最后换行符为两个: \r\n
            each = each + '\"'
        txt_trans = txt_trans + each + ','
    txt_trans = txt_trans[0:len(txt_trans) - 1] + '}'
    file_txt.close()
    return json.loads(txt_trans)


def get_header_info(path_header, path_userAgent=None, path_proxy=None):
    web_header = read_txt2json(path_header)
    if path_userAgent is not None:
        userAgent, userAgentLib = user_agent(path_userAgent)
        web_header['User-Agent'] = userAgent
    if path_proxy is not None:
        userProxy, userProxyLib = user_proxy(path_proxy)
        proxy_handler = urllib.request.ProxyHandler(userProxy)
        url_opener = urllib.request.build_opener(proxy_handler)
        print(userProxy)
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

    def form_data_encryption(self, req_str):
        ts = str(int(time.time() * 1000))  # 毫秒时间戳
        salt = ts + str(random.randint(1, 10))  # 加密用的盐
        sign = hashlib.md5(("fanyideskweb" + req_str + salt +
                           "n%A-rKaT5fb[Gy?;N5@Tj").encode('utf-8')).hexdigest()
        # 签名字符串
        return {"ts": ts,
                "salt": salt,
                "sign": sign}

    def post_method(self, path_formData,
                    change_dic, path_comp_table=None):
        form_data = read_txt2json(path_formData)
        # form_data['i'] = req_str
        post_data = self.form_data_encryption(change_dic['i'])
        for key, value in post_data.items():
            form_data[key] = post_data[key]
        for key, value in change_dic.items():
            form_data[key] = change_dic[key]
        if path_comp_table is not None:
            comp_table = read_txt2json(path_comp_table)
            for each_key in comp_table['change_key']:
                form_data[each_key] = comp_table[form_data[each_key]]
        data = urllib.parse.urlencode(form_data).encode(encoding='utf8')
        req = urllib.request.Request(self.url, data=data, headers=self.web_header)
        response = urllib.request.urlopen(req)
        html_code = response.read()
        return html_code


def write_html_code(html_code, path_phpFile):
    phpFile = open(path_phpFile, 'wb')
    phpFile.write(html_code)
    phpFile.close()
