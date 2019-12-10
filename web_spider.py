# coding=UTF-8<code>
import requests
import csv
import random
import time
import socket
import http.client
import urllib.request
from bs4 import BeautifulSoup
import re
import json


class WeatherDataCollection(object):
    def __init__(self, web_url, path_header):
        self.web_url = web_url
        self.path_header = path_header

    def __path_json2dict(self):
        file_header = open(self.path_header, 'r')
        # 打开读取保存网页header文件
        WebHeader: str = file_header.read()
        self.web_header = json.loads(WebHeader)
        # print(WebHeader, '--', type(WebHeader))
        file_header.close()

    def get_html_code(self):  # 抓取网页源码，获取数据
        self.__path_json2dict()
        timeout = random.choice(range(80, 180))
        html = requests.get(self.web_url, headers=self.web_header, timeout=timeout)
        # html.encoding = 'utf-8'
        return html.text

    def get_data(self):  # 清洗数据
        html_code = self.get_html_code()
        bs = BeautifulSoup(html_code, 'html.parser')
        body = bs.body
        html_data = body.find('div', {'id': '7d'})
        ul = html_data.find('ul')
        li = ul.find_all('li')

        weather_data = []
        for day in li:
            WeatherData_temp = []
            date = day.find('h1').string
            WeatherData_temp.append(date)
            inf = day.find_all('p')
            WeatherData_temp.append(inf[0].string)
            if inf[1].find('span') is None:
                temperature_highest = None
            else:
                temperature_highest = inf[1].find('span').string
                temperature_highest = temperature_highest.replace('℃', '')
            temperature_lowest = inf[1].find('i').string
            temperature_lowest = temperature_lowest.replace('℃', '')
            WeatherData_temp.append(temperature_highest)
            WeatherData_temp.append(temperature_lowest)
            weather_data.append(WeatherData_temp)

        return weather_data

    def write_data(self, file_name):
        inf_data = self.get_data()
        with open(file_name, 'a', newline='') as f:
            csvFile = csv.writer(f)
            csvFile.writerows(inf_data)
            f.close()


class TaoBaoDataCollection(WeatherDataCollection):
    def match_inf(self, html_code):
        html_info = re.search(r'g_page_config = (.*?)}};', html_code)
        html_info_str = html_info.group(1) + "}}"
        html_info_json = json.loads(html_info_str)
        return html_info_json

    def get_data(self):
        html_code = self.get_html_code()
        good_json = self.match_inf(html_code)
        good_items = good_json['mods']['itemlist']['data']['auctions']

        good_list = [['商品名称', '价格', '运费',
                     '销量', '位置', '链接']]
        for each in good_items:
            # 将链接字符串前统一为http:...
            str_loc = each['comment_url'].find('//')
            each['comment_url'] = 'https:' + each['comment_url']\
                [str_loc:len(each['comment_url'])]
            # 将销量统一为float类型
            # 判断位置：Python中[a, b]是左闭右开型，不包括b位置
            if each['view_sales'].find('万') is not -1:
                str_loc1 = each['view_sales'].find('万')
                each['view_sales'] = float(each['view_sales'][0:str_loc1])*1e4
            elif each['view_sales'].find('+') is not -1:
                str_loc1 = each['view_sales'].find('+')
                each['view_sales'] = float(each['view_sales'][0:str_loc1])
            elif each['view_sales'].find('人') is not -1:
                str_loc1 = each['view_sales'].find('人')
                each['view_sales'] = float(each['view_sales'][0:str_loc1])
            good_temp = \
                [each['raw_title'], each['view_price'],
                 each['view_fee'], each['view_sales'],
                 each['item_loc'], each['comment_url']]
            good_list.append(good_temp)
        return good_list


# # 爬取中国天气网信息
# WebUrl = r'http://www.weather.com.cn/weather/101210101.shtml'  # 101210101：杭州， 101180301：新乡
# PathHeader = r'F:\Python Study\Myconda\urlStudy_doc\WebHeader.txt'
# weatherFileName = r'F:\Python Study\Myconda\urlStudy_doc\WeatherData.csv'
# weather = WeatherDataCollection(WebUrl, PathHeader)
# htmlCode = weather.get_html_code()
# weatherData = weather.get_data()
# # weather.write_data(weatherFileName)
#
# # 爬取淘宝网商品信息
WebUrl = r'https://s.taobao.com/search?q=%E8%87%AA%E7%83%AD%E5%B0%8F%E7%81%AB%E9%94%85'
PathHeader = r'F:\Python Study\Myconda\urlStudy_doc\WebHeader_taobao.txt'
taobaoFileName = r'F:\Python Study\Myconda\urlStudy_doc\TaoBaoData.csv'
taobao = TaoBaoDataCollection(WebUrl, PathHeader)
htmlCode = taobao.get_html_code()
print(htmlCode)
# TaoBaoData = taobao.get_data()
# print(TaoBaoData)
# taobao.write_data(taobaoFileName)

# 爬取百度文库信息 WebUrl = r'https://wenku.baidu.com/view/ec14da6703020740be1e650e52ea551810a6c9cc.html?rec_flag=default
# &sxts=1574584527981' PathHeader = r'C:\Users\Admin\Desktop\WebHeader_wenku.txt' wenku = WeatherDataCollection(
# WebUrl, PathHeader) htmlCode = wenku.get_html_code() print(htmlCode)
