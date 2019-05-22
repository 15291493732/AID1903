"""
聊天室服务端
Chat room
env:python3.6
socket server
"""
from socket import *
import os, sys

Addr = ('0.0.0.0', 8888)  # 服务器地址
# 存储用户信息
user = {}


# 进入聊天室
def do_login(s, name, addr):
    if name in user or "管理员" in name:
        s.sendto("该用户已存在".encode(), addr)
        return
    s.sendto(b'ok', addr)
    msg = "欢迎%s进入聊天室" % name  # 通知其他人
    for i in user:
        s.sendto(msg.encode(), user[i])
    # 将用户加入
    user[name] = addr
    print(user)


# 聊天功能
def do_chat(s, name, text):
    msg = "%s:%s" % (name, text)
    for i in user:
        if i != name:
            s.sendto(msg.encode(), user[i])


# 退出
def do_quit(s, name):
    msg = "%s退出了聊天室" % name
    for i in user:
        if i != name:
            s.sendto(msg.encode(), user[i])
        else:
            s.sendto(b'EXIT', user[i])
    # 将用户删除
    del user[name]
    print(user)


# 循环接收客户端请求Q
def do_request(s):
    while True:
        data, addr = s.recvfrom(1024)
        msg = data.decode().split(' ')
        # 区分请求类型
        if msg[0] == 'L':
            do_login(s, msg[1], addr)
        elif msg[0] == 'C':
            text = ' '.join(msg[2:])
            do_chat(s, msg[1], text)
        elif msg[0] == 'Q':
            if msg[1] not in user:
                s.sendto(b'EXIT', addr)
                continue
            do_quit(s, msg[1])


# 创建网络连接
def main():
    # 创建面向无连接数据报udp套接字
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(Addr)

    pid = os.fork()
    if pid < 0:
        return
    # 发管理员消息
    elif pid == 0:
        while True:
            msg = input("管理员消息：")
            msg = "C 管理员消息 " + msg
            s.sendto(msg.encode(), Addr)
    else:
        # 请求处理
        do_request(s)  # 处理客户端请求
    # 请求处理
    do_request(s)  # 处理客户端请求


if __name__ == '__main__':
    main()
