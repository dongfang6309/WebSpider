# coding=UTF-8<code>
import urllib.request
import urllib.parse
import re
import json
import time
import urllib_func as urf
from pypinyin import pinyin, Style


def get_url(url, req_str, page):
    wd = {'kw': req_str}
    url_tem = url + urllib.parse.urlencode(wd) + '&pn=' + str((page-1)*50)
    return url_tem


def get_spider(url, req_str, page_ini, page_end,
               path_header, path_userAgent, path_proxy, path_phpFile):
    web_header, url_opener = urf.get_header_info(path_header, path_userAgent, path_proxy)
    print(web_header['User-Agent'])
    req_str_pin = pinyin(req_str, style=Style.NORMAL)
    req_piny = ''
    for each in req_str_pin:
        req_piny = req_piny + each[0]
    for page in range(page_ini, page_end + 1):
        url_tem = get_url(url, req_str, page)
        html_code_temp = urf.get_html_code(url_tem, web_header, url_opener)
        path_phpFile_tem = path_phpFile + r'\%s_tieba_page%d.php' % (req_piny, page)
        print('正在下载%s贴吧第%d页' % (req_str, page))
        urf.write_html_code(html_code_temp, path_phpFile_tem)


if __name__ == "__main__":
    req_str = input('请输入贴吧名称\n')
    page_ini = int(input('请输入起始页码\n'))
    page_end = int(input('请输入终止页码\n'))

    url = r'http://tieba.baidu.com/f?'
    path_userAgent = r'.\urlStudy_doc\UserAgentLib.txt'
    path_proxy = r'.\urlStudy_doc\ProxyLib.txt'
    path_header = r'.\urlStudy_doc\WebHeader_baidu.txt'
    path_phpFile = r'D:\phpStudy\WWW\Demo\jiahao_test1'

    get_spider(url, req_str, page_ini, page_end,
               path_header, path_userAgent, path_proxy, path_phpFile)
    # time.sleep(6)
