# coding=UTF-8<code>
import urllib.request
import urllib.parse
import urllib_func as urf
import re

req_str = '大学'
url = r'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
path_header = r'.\urlStudy_doc\WebHeader_youdao.txt'
path_formData = r'.\urlStudy_doc\FormData_youdao.txt'

web_header, url_opener = urf.get_header_info(path_header)
print(web_header['User-Agent'])
html_code = urf.GetHtmlCode(url, web_header, url_opener).post_method(req_str, path_formData)
print(html_code.decode())

# find_info = r'{"tgt":"(.*?)","src"'
# html_info = re.search(find_info, html_code.decode())
# html_info_str = html_info.group(1)
# print(html_info, '\t----', type(html_info))
# print(html_info_str, '\t----', type(html_info_str))
