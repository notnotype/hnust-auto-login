# 你看我像是写文档的人吗(hnust校园网自动登录脚本)
> 校园网每一次连接又要登录,觉得不爽,写个小脚本来实现自动登录
## 快速开始
- 安装python环境(可以直接通过exe可执行文件运行)
- 安装依赖
- 部署到启动目录   

## 安装依赖
```bash
pip install -r requirements.txt
```
## 部署与使用
程序有两种启动方法
* 使用python解释器来使用
* 直接使用通过pyinstaller打包好了的exe可执行文件运行

#### 一, 使用python解释器
在安装好了python解释器之后,打开命令行输入来登录校园网

```bash
python hnust login
```
> 若你这么做了,程序会询问你的密码和账号,你不用担心你的密码会被泄露.
> 因为这个软件是一个开源软件, 你随时拥有可以查看该软件源代码的权利.
> 因此不必担心我回到去你的密码

#### 二, 使用exe可执行文件启动
同样的, 软件的功能是一样的只是运行效率稍微低了
输入以下命令来运行软件
```bash
./hnust.exe login
```

## 功能
当你在控制台输入```python hnust.py --help```的时候
你会得到一下内容
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