# coding=UTF-8<code>
import urllib.request
import re
import json
import random

path_userAgent = r'F:\Python Study\Myconda\urlStudy_doc\UserAgentLib.txt'
path_proxy = r'F:\Python Study\Myconda\urlStudy_doc\ProxyLib.txt'
url = r'http://www.baidu.com/'

file_userAgent = open(path_userAgent, 'r')
userAgentLib = []
for line in file_userAgent.readlines():
    line = line.strip()
    userAgentLib.append(line)
file_userAgent.close()
userAgent = random.choice(userAgentLib)
web_header = {
    "User-Agent": userAgent
}

file_proxy = open(path_proxy)
userProxyLib = file_proxy.read()
file_proxy.close()
# print(userProxyLib)
userProxyLib = json.loads(userProxyLib)
userProxy = random.choice(userProxyLib)
print(userProxy)

# 构建HTTP处理器对象
http_handler = urllib.request.HTTPHandler()
# 构建Proxy处理器对象
proxy_handler = urllib.request.ProxyHandler(userProxy)
# 创建自定义opener
# url_opener = urllib.request.build_opener(http_handler)
url_opener = urllib.request.build_opener(proxy_handler)
# 设置opener为全局，这样用urlopen发送的请求也会使用自定义opener
urllib.request.install_opener(url_opener)

# 将url进行封装，变为Request对象
req = urllib.request.Request(url, headers=web_header)
# # response = url_opener.open(req)
response = urllib.request.urlopen(req)
html_code = response.read()
# # html_code = urllib.request.urlopen(url).read()
print(html_code.decode())
print(type(html_code))
print(type(html_code.decode()))
print(response.getcode())

find_info = r'<title>(.*?)</title>'
# find_info = r'<span class="bg s_btn_wr"><input type="submit" id="su" value="(.*?)" class="bg s_btn">'

# mode:findall
# html_info = re.findall(find_info, html_code.decode())
# html_info_str = html_info[0]
# print(html_info, '\t----', type(html_info))
# print(html_info_str, '\t----', type(html_info_str))

# mode:search
html_info = re.search(find_info, html_code.decode())
html_info_str = html_info.group(1)
print(userAgent)
print(html_info, '\t----', type(html_info))
print(html_info_str, '\t----', type(html_info_str))
print(userProxy)
