"""
聊天室客户端
Chat room
env:python3.6
socket cline
"""
from socket import *
import os, sys

# 服务器地址
Addr = ('127.0.0.1', 8888)


# 发送消息
def send_msg(s, name):
    while True:
        # 如果客户端关闭也退出
        try:
            text = input("发言:")
        except KeyboardInterrupt:
            text = 'quit'
        # 退出聊天室
        if text == 'quit':
            msg = "Q " + name
            s.sendto(msg.encode(), Addr)
            sys.exit("退出聊天室")

        msg = "C %s %s" % (name, text)
        s.sendto(msg.encode(), Addr)


# 接收消息
def recv_msg(s):
    while True:
        try:
            data, addr = s.recvfrom(2048)
        except KeyboardInterrupt:
            break
        # 服务端发送EXIT表示让客户端退出
        if data.decode() == 'EXIT':
            sys.exit()
        print(data.decode())


# 创建网络连接
def main():
    s = socket(AF_INET, SOCK_DGRAM)
    while True:
        try:
            name = input("请输入姓名：")
        except KeyboardInterrupt:
            return
        msg = "L " + name
        print(msg)
        s.sendto(msg.encode(), Addr)
        # 等待接收回应
        data, addr = s.recvfrom(1024)
        if data.decode() == 'ok':
            print("您已进入聊天室")
            break
        else:
            print(data.decode())
    # 创建新的进程
    pid = os.fork()
    if pid < 0:
        sys.exit('Error')
    elif pid == 0:
        send_msg(s, name)
        print(name)
    else:
        recv_msg(s)


if __name__ == '__main__':
    main()
