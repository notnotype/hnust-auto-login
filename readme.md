# hnust校园网自动登录脚本
> 校园网每一次连接又要登录,觉得不爽,写个小脚本来实现自动登录

# 新手看这里, 老手跳过
- 下载`hnust.exe`
- `win`键+`r`输入`cmd`打开终端
- 使用`cd`命令把工作目录切换到你刚刚下载的文件目录下
> 不会使用请自行百度 `cmd常用命令`
- 输入 `hnust.exe login` 来使用


## 快速开始
- 安装`Python`环境(可以直接通过`exe`可执行文件运行)
- 安装依赖
- 部署到启动目录   
------
##### 一键脚本
```bash
git clone https://github.com/notnotype/hnust-auto-login.git
cd hnust-auto-login
pip install -r requirements.txt
python hnust.py login
```

## 安装依赖
```bash
pip install -r requirements.txt
```
## 部署与使用
程序有两种启动方法
* 使用```Python```解释器来使用
* 直接使用通过```pyinstaller```打包好了的```exe```可执行文件运行

#### 一, 使用`Python`解释器
在安装好了python解释器之后,打开命令行输入来登录校园网

```bash
python hnust.py login
```
> 若你这么做了,程序会询问你的密码和账号,你不用担心你的密码会被泄露.
> 因为这个软件是一个开源软件, 你随时拥有可以查看该软件源代码的权利.
> 因此不必担心我会盗取你的密码

#### 二, 使用`exe`可执行文件启动
同样的, 软件的功能是一样的只是运行效率稍微低了,
输入以下命令来运行软件

```bash
./hnust.exe login
```

## 功能
当你在控制台输入```python hnust.py --help```的时候
你会得到以下内容

```bash
Usage: hnust.py [OPTIONS] COMMAND [ARGS]...

  当遇到bug时尝试重新输入密码登录 运行`python login`

Options:
  --help  Show this message and exit.

Commands:
  addstartup  把这个程序添加到开机启动里面 这样每次开机就能够自动检测登录了
  getinfo     【没写】 返回网页包含了用户网络信息，使用re库来获取script标签里面的变量
  login       用校园网用户名（学号）和校园网密码登录校园网
  logout      退出登录
```
命令指南已经写的很明了了,我也没必要在这里多说废话了
唯一值得注意的是命令```addstartup```
这一条命令需要使用管理员的身份运行才能够成功

## 原理
自己看源码,我相信你看的懂的
简单解释一下:
就是使用`Python`发送表单给`login.hunst.cn`
`login.hunst.cn`接受到了以后就会给我们分配网络资源
下面的就是关键代码 -- 调用`api`

```python
r = get(f"http://login.hnust.cn:801/eportal/?c=Portal&a=login&callback=dr1004&login_method=1&user_account=%2C0" +
f"%2C{username}%40telecom&user_password={password}&wlan_user_ip={getIp()}&wlan_user_ipv6" +
f"=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=3.3.3&v={random.randint(1000, 9999)}",timeout=5)
```
## 如何编译
因为被`pyinstaller`编译后的可执行文件很大,所以`exe`文件不能够得到及时的更新,所以可以手动编译
运行一下命令来编译
```bash
pip install pyinstaller
pyinstaller hnust.py     #生成一个文件夹
pyinstaller -F hnust.py  #生成单个文件 
```
编译后的可执行文件在`dist/hnust/hnust.exe`位置
编译后的可执行文件在`dist/hnust.exe`位置

## 未来
* 完善命令`pyton hnust.py getinfo`获取当前设备的信息
