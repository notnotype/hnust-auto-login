import os
import random
import sys

import click
import socket
from requests import get
from requests.exceptions import ConnectionError, ConnectTimeout

headers = {
    "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " +
                  "Chrome/86.0.4240.111 Safari/537.36"}


def getIp():
    """
    查询本机ip地址
    :return: ip
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('192.168.254.226', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def isInternetAccess():
    successCount = 0
    for i in range(2):
        try:
            successCount += 0 if "<title>上网登录页</title>" in get("http://www.baidu.com", timeout=2).text else 1
        except:
            pass
    return True if successCount >= 1 else False


def getProperties(prop):
    f = open("./.config", "a")
    f.close()
    kv = {}
    f = open("./.config", "r")
    for line in f:
        temp = line.split("=")
        kv[temp[0].strip()] = temp[1].strip()
    f.close()
    return kv[prop] if prop in kv else ""


def setProperties(key, value):
    key, value = str(key), str(value)
    kv = {}
    f = open("./.config", "r")
    for line in f:
        temp = line.split("=")
        kv[temp[0].strip()] = temp[1].strip()
    kv[key] = value
    f.close()
    f = open("./.config", "w+")
    for k, v in kv.items():
        f.write(k + " = " + v)
        f.write("\n")
    f.close()


@click.group()
def cli():
    """当遇到bug时尝试重新输入密码登录 运行`python login`"""
    pass


# noinspection PyBroadException
@click.command()
@click.option("--username", prompt="你的学号", default=getProperties("username"))
@click.option("--password", hide_input=True, prompt="你的校园网密码",
              default=("*" * len(getProperties("password")) if getProperties("password") else None))  # 能够回车直接输入默认值
@click.option("--operator", prompt="运营商选择[dx,yd,lt,xyw]", default=getProperties("operator"))
def login(username, password, operator):
    """
    用校园网用户名（学号）和校园网密码登录校园网
    """
    # 因为密码是不能给别人看见的，所有要在这里检测缓存的密码

    if password == "*" * len(getProperties("password")) or password is None:
        password = getProperties("password")

    setProperties("username", username)
    setProperties("password", password)
    setProperties("operator", operator)

    operatorMap = {"dx": "%40telecom", "yd": "%40cmcc", "lt": "%40unicom", "xyw": ""}

    retry = 0
    # todo抽象成一个方法来检测是否能上网
    while True:  # 检测是否能够连接上网
        try:
            resp = get(
                f"http://login.hnust.cn:801/eportal/?c=Portal&a=login&callback=dr1004&login_method=1&user_account=%2C0" +
                f"%2C{username}{operatorMap[operator]}&user_password={password}&wlan_user_ip={getIp()}&wlan_user_ipv6" +
                f"=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=3.3.3&v={random.randint(1000, 9999)}",
                # 防止缓存
                timeout=5)
            if resp.text == r'dr1004({"result":"1","msg":"\u8ba4\u8bc1\u6210\u529f"})':
                message = f"[登录状态]: 登录成功: 运营商是: [{operator}]"
                click.echo(message)
            elif resp.text == r'dr1004({"result":"0","msg":"","ret_code":2})':
                message = "[登录状态]: 已经登录了"
                click.echo(message)
                click.echo("退出登录中......")
                _logOut()
                continue  # 都已经退出登录了,就不要在检测是否可以连接至internet了
            elif "dXNlcmlkIGVycm9y" in resp.text:  # 检测userid error是否在返回值里面
                message = "[登录状态]: 密码错误(检查是否有绑定运营商账号)"
                click.echo(message)
                break
            elif r"\u5bc6\u7801\u4e0d\u80fd\u4e3a\u7a7a" in resp.text:
                message = "[登录状态]: 密码不能为空"
                click.echo(message)
                break
            else:
                message = "[登录状态]: 芜湖, 有bug了: " + resp.text
                click.echo(message)
                break

            click.echo("检测是否可以连接到互联网......")
            if isInternetAccess():
                click.echo("可以连接互联网  登陆成功")
                return
            else:
                if retry >= 3:
                    click.echo("该账号不能连接至Internet(你可能使用校园网登录,因此不能连接至互联网)")
                    return
                click.echo("不能连接互联网, 重试")
                retry += 1
        except ConnectTimeout:
            message = "超时(你可能没有连接校园网wifi)"
        except ConnectionError:
            message = "找不到主机(你可能没有连接校园网wifi)"
        except BaseException as e:
            message = f"未知错误[{type(e)}]：\n" + str(e)




# todo 返回网页包含了用户网络信息，使用re库来获取script标签里面的变量
@click.command()
def getInfo():
    """
    【没写】
    返回网页包含了用户网络信息，使用re库来获取script标签里面的变量
    """
    resp = get("http://login.hnust.cn/?isReback=1")
    print(resp.text)


def _logOut():
    try:
        resp = get(f"http://login.hnust.cn:801/eportal/?c=Portal&a=logout&callback=dr1003&login_method=1&user_account" +
                   f"=drcom&user_password=123&ac_logout=0&register_mode=1&wlan_user_ip={getIp()}&wlan_user_ipv6" +
                   f"=&wlan_vlan_id=1&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=3.3.3&v="
                   f"{random.randint(1000, 9999)}",
                   timeout=5)
        if resp.text == r'dr1003({"result":"0","msg":"\u6ce8\u9500\u5931\u8d25"})':
            message = "注销失败(你可能已经注销了)"
        elif resp.text == r'dr1003({"result":"1","msg":"\u6ce8\u9500\u6210\u529f"})':
            message = f"IP：【{getIp()}】注销成功"
        else:
            message = "芜湖, 有bug了: " + resp.text
    except ConnectTimeout:
        message = "超时(你可能没有连接校园网wifi)"
    except ConnectionError:
        message = "找不到主机(你可能没有连接校园网wifi)"
    except BaseException as e:
        message = f"未知错误[{type(e)}]：\n" + str(e)
    click.echo(message)


# noinspection PyBroadException
@click.command()
@click.confirmation_option(prompt=f"你确定要注销登陆【你当前IP为：{getIp()}】", default=True)
def logOut():
    """退出登录"""
    _logOut()


# noinspection PyBroadException
@click.command()
def addStartup():
    """把这个程序添加到开机启动里面 这样每次开机就能够自动检测登录了"""

    try:
        os.popen("explorer.exe \"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp")
        click.echo("记得使用管理员的身份运行")
        cmd1 = f"copy hnust.py \"C:\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\hnust.py\""
        cmd2 = f"copy .config \"C:\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\.config\""
        cmd3 = f"copy hnust.exe \"C:\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\hnust.exe\""

        click.echo("cmd1: " + cmd1)
        click.echo("cmd2: " + cmd2)
        click.echo("cmd3: " + cmd3)

        result1 = os.popen(
            cmd1).read()
        result2 = os.popen(
            cmd2).read()
        result3 = os.popen(
            cmd3).read()
        click.echo(result1)
        click.echo(result2)
        click.echo(result3)

    except IOError as e:
        click.echo("Unable to copy file. %s" % e)
    except BaseException:
        click.echo("Unexpected error:", sys.exc_info())


cli.add_command(login)
cli.add_command(logOut)
cli.add_command(getInfo)
cli.add_command(addStartup)

if __name__ == '__main__':
    if "StartUp" in sys.argv[0] and len(sys.argv) <= 1:  # 如果在启动目录下则自动检测登录
        sys.argv = [sys.argv[0], "login",
                    "--username", getProperties("username") if getProperties("username") else None,
                    "--password", getProperties("password") if getProperties("password") else None,
                    "--operator", getProperties("operator") if getProperties("operator") else None,
                    ]
    cli()
