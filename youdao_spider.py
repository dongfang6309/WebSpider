# coding=UTF-8<code>
import urllib.request
import urllib.parse
import urllib_func as urf
import re

req_str = 'Python爬虫有道翻译，真香！'
url = r'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
path_header = r'.\urlStudy_doc\WebHeader_youdao.txt'
path_formData = r'.\urlStudy_doc\FormData_youdao2.txt'
path_userAgent = r'.\urlStudy_doc\UserAgentLib.txt'
path_proxy = r'.\urlStudy_doc\ProxyLib.txt'

web_header, url_opener = urf.get_header_info(path_header, path_userAgent, path_proxy)
print(web_header['User-Agent'])
html_code = urf.GetHtmlCode(url, web_header, url_opener)\
    .post_method(req_str, path_formData)
print(html_code.decode())

find_info = r'{"tgt":"(.*?)","src"'
html_info = re.search(find_info, html_code.decode())
html_info_str = html_info.group(1)
# print(html_info, '\t----', type(html_info))
print('\033[1;35m %s\033[0m' % html_info_str, '\t----', type(html_info_str))
