#!/usr/bin/env python3

import os
import re
import time

import requests


def main() -> int:
    n_retry = 3

    print("\n\n==============")
    print("""
    注意!!
    首先连接上WiFi “csust—bg” 或者插上办公区的网线\n
    """)
    print("本程序仅供学习用途\n")
    print("=============\n")

    id, password = load_account()
    print(f"登录帐号：{id}")

    for i in range(1, n_retry + 1):
        if is_online():
            print(f"==> 网络已连接")
            return 0

        print(f"==> 第 {i} 次 尝试")

        login(id, password)

    return 1


def login(id, password):
    url = "http://1.1.1.1"
    try:
        a = requests.get(url=url, allow_redirects=False, timeout=5)
        url2 = a.headers["Location"]
        print(url2)
        b = str(url2).split("&")
        wlanuserip = ""
        wlanacname = ""
        wlanacip = ""
        wlanusermac = ""

        for i in b:
            if "wlanuserip" in i:
                wlanuserip = i.split("=")[-1]
            elif "wlanacip" in i:
                wlanacip = i.split("=")[-1]
            elif "wlanacname" in i:
                wlanacname = i.split("=")[-1]
            elif "wlanusermac" in i:
                wlanusermac = i.split("=")[-1][:12]
                wlanusermac = re.findall(r"\w{1,2}", wlanusermac)
                wlanusermac = "-".join(wlanusermac)
        print("获取相关信息中")
        print("====================================")
        print("路由器网关地址:" + wlanuserip)
        print("连接路由器型号:" + wlanacname)
        print("用户IP地址:" + wlanacip)
        print("路由器MAC地址:" + wlanusermac)
        print("====================================")
        time.sleep(1)
        print("开始尝试登陆~~~")
        time.sleep(2)
        post_url = "http://192.168.7.221:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=192.168.7.221&iTermType=1&wlanuserip={wlanuserip}&wlanacip={wlanacip}&wlanacname={wlanacname}&mac={wlanusermac}&ip={wlanuserip}&enAdvert=0&queryACIP=0&loginMethod=1".format(
            wlanusermac=wlanusermac,
            wlanacip=wlanacip,
            wlanacname=wlanacname,
            wlanuserip=wlanuserip,
        )
        data = {
            "DDDDD": ",0,{}".format(id),
            "upass": "{}".format(password),
            "R1": "0",
            "R2": "0",
            "R3": "0",
            "R6": "0",
            "para": "00",
            "0MKKey": "123456",
        }
        requests.post(url=post_url, data=data)
        check()
    except:
        print("发起网络请求失败")
        print("请检查网络是否能访问 1.1.1.1 和 192.168.7.221")


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
