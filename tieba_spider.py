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


def get_header_info(path_header, path_userAgent, path_proxy):
    userAgent, userAgentLib = urf.user_agent(path_userAgent)
    userProxy, userProxyLib = urf.user_proxy(path_proxy)
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


def write_html_code(html_code, path_phpFile, page):
    phpFile = open(path_phpFile, 'wb')
    phpFile.write(html_code)
    phpFile.close()


def get_spider(url, req_str, page_ini, page_end,
               path_header, path_userAgent, path_proxy, path_phpFile):
    web_header, url_opener = get_header_info(path_header, path_userAgent, path_proxy)
    print(web_header['User-Agent'])
    req_str_pin = pinyin(req_str, style=Style.NORMAL)
    req_piny = ''
    for each in req_str_pin:
        req_piny = req_piny + each[0]
    for page in range(page_ini, page_end + 1):
        url_tem = get_url(url, req_str, page)
        html_code_temp = get_html_code(url_tem, web_header, url_opener)
        path_phpFile_tem = path_phpFile + r'\%s_tieba_page%d.php' % (req_piny, page)
        print('正在下载%s贴吧第%d页' % (req_str, page))
        write_html_code(html_code_temp, path_phpFile_tem, page)


if __name__ == "__main__":
    req_str = input('请输入贴吧名称\n')
    page_ini = int(input('请输入起始页码\n'))
    page_end = int(input('请输入终止页码\n'))

    url = r'http://tieba.baidu.com/f?'
    path_userAgent = r'H:\MyPythonCode\WebSpider\urlStudy_doc\UserAgentLib.txt'
    path_proxy = r'H:\MyPythonCode\WebSpider\urlStudy_doc\ProxyLib.txt'
    path_header = r'H:\MyPythonCode\WebSpider\urlStudy_doc\WebHeader_baidu.txt'
    path_phpFile = r'E:\phpStudy\WWW\Demo\tieba_spider'

    get_spider(url, req_str, page_ini, page_end,
               path_header, path_userAgent, path_proxy, path_phpFile)
    # time.sleep(6)
