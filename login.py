#!/usr/bin/env python3

import os
import time
from urllib.parse import urlparse, parse_qs

import requests


def main() -> int:
    n_retry = 3
    id, password = load_account()
    print(f"登录帐号：{id}")

    for i in range(1, n_retry + 1):
        if is_online():
            print(f"==> 网络已连接")
            return 0

        print(f"==> 第 {i} 次 尝试")

        if login(id, password):
            print("==> 登录成功")
        else:
            print("==> 登录失败")

    return 1


def login(id, password) -> bool:
    url = "http://1.1.1.1"
    try:
        a = requests.get(url=url, allow_redirects=False, timeout=5)
        url2 = a.headers["Location"]
        print(url2)

        parsed = urlparse(url2)
        info = parse_qs(parsed.query)
        userip = info['wlanuserip'][0]
        acname = info['wlanacname'][0]
        acip = info['wlanacip'][0]
        usermac = info['wlanusermac'][0]

        print("获取相关信息中")
        print("====================================")
        print("路由器网关地址:" + userip)
        print("连接路由器型号:" + acname)
        print("用户IP地址:" + acip)
        print("路由器MAC地址:" + usermac)
        print("====================================")
        time.sleep(1)
        print("开始尝试登陆~~~")
        login_url = f"https://login.csust.edu.cn:802/eportal/portal/login?callback=dr1003&login_method=1&user_account=%2C0%2C{id}&user_password={password}&wlan_user_ip={userip}&wlan_user_ipv6=&wlan_user_mac={usermac}&wlan_ac_ip={acip}&wlan_ac_name={acip}&jsVersion=4.2.1&terminal_type=1&lang=zh-cn&v=2625&lang=zh"
        r = requests.get(login_url)
        msg = r.content.decode('utf-8')
        print(f"==> 登录信息：{msg}")

        return "成功" in msg

    except:
        print("发起网络请求失败")
        print("请检查网络是否能访问 1.1.1.1 和 192.168.7.221")

    return True


def is_online():
    print("检查网络中~~~~~~,请稍后")
    try:
        a = requests.get("https://www.baidu.com", timeout=1).text
    except:
        a = "0"
    if "About Baidu" in a:
        print("\n==============")
        print("     登录成功")
        print("    程序准备退出")
        print("=============\n")
        return True
    else:
        return False


def load_account():
    account_file_path = f"{os.path.realpath(os.path.dirname(__file__))}/account.txt"

    with open(account_file_path, "r") as fd:
        id = fd.readline().rstrip()
        password = fd.readline().rstrip()

    return id, password


if __name__ == "__main__":
    exit(main())
