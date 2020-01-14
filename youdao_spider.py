# coding=UTF-8<code>
import urllib.request
import urllib.parse
import urllib_func as urf
import re

# req_str = 'Python爬虫，真香！'
with open(r'F:\Python Study\WebSpider\urlStudy_doc\req_str_youdao.txt',
          'rb') as f:
    req_str = f.read().decode()
lang_from = '中文'  # ''为自动检测: AUTO
lang_to = ['英语', '韩语', '法语', '俄语']

url = r'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
path_header = r'.\urlStudy_doc\WebHeader_youdao.txt'
path_formData = r'.\urlStudy_doc\FormData_youdao2.txt'
path_userAgent = r'.\urlStudy_doc\UserAgentLib.txt'
path_proxy = r'.\urlStudy_doc\ProxyLib.txt'
diff_lang = r'.\urlStudy_doc\DiffLanguage_youdao.txt'

web_header, url_opener = urf.get_header_info(path_header, path_userAgent, path_proxy)
print(web_header['User-Agent'])
for each_lang_to in lang_to:
    change_dic = {"i": req_str,
                  "from": lang_from,
                  "to": each_lang_to}
    html_code = urf.GetHtmlCode(url, web_header, url_opener) \
        .post_method(path_formData, change_dic, diff_lang)
    # print(html_code.decode())

    find_info = r'{"tgt":"(.*?)","src"'
    # html_info = re.search(find_info, html_code.decode())
    # html_info_str = html_info.group(1)
    # print(html_info_str, '\t----', type(html_info_str))
    # 由于存在多个带翻译语句，所以搜索结果使用find_all模式
    html_info = re.findall(find_info, html_code.decode())
    html_info_str = ''
    for each in html_info:
        html_info_str = html_info_str + ' ' + each
    print('%s为:' % each_lang_to,
          '\033[1;35m %s\033[0m' % html_info_str)
