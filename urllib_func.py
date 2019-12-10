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
