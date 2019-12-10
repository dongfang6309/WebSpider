# coding=UTF-8<code>
import urllib.request
import urllib.parse
import re
import random
import json
import urllib_func as urf

# 构造url编码
url = r'http://www.baidu.com/s?'
# url = r'http://www.baidu.com/'
req_str = '张佳豪'
wd = {'wd': req_str}
url = url + urllib.parse.urlencode(wd)

path_userAgent = r'F:\Python Study\Myconda\urlStudy_doc\UserAgentLib.txt'
path_proxy = r'F:\Python Study\Myconda\urlStudy_doc\ProxyLib.txt'
userAgent, userAgentLib = urf.user_agent(path_userAgent)
userProxy, userProxyLib = urf.user_proxy(path_proxy)

path_header = r'F:\Python Study\Myconda\urlStudy_doc\WebHeader_baidu.txt'
file_header = open(path_header, 'r')
WebHeader: str = file_header.read()
web_header = json.loads(WebHeader)
# print(WebHeader, '--', type(WebHeader))
file_header.close()
# web_header['User-Agent'] = userAgent

proxy_handler = urllib.request.ProxyHandler(userProxy)
http_handler = urllib.request.HTTPHandler()
url_opener = urllib.request.build_opener(http_handler)
urllib.request.install_opener(url_opener)

# 进行get请求
req = urllib.request.Request(url, headers=web_header)
response = urllib.request.urlopen(req)
html_code = response.read()
print(html_code.decode())
print(url)
print(userAgent, '\n', userProxy)

# 将网页写入php文件
path_phpFile = r'D:\phpStudy\WWW\Demo\Jiahao_test1\Baidu_test.php'
phpFile = open(path_phpFile, 'wb')
phpFile.write(html_code)
phpFile.close()

# 正则匹配title信息
find_info = r'<title>(.*?)</title>'
html_info = re.search(find_info, html_code.decode())
html_info_str = html_info.group(1)
print(html_info, '\t----', type(html_info))
print(html_info_str, '\t----', type(html_info_str))
