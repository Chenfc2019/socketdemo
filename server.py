#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : server.py
# @Author: Small-orange
# @Date  : 2020-3-10
# @Desc  : 服务端，接收客户端上传的数据

import socket
from threading import Thread

addr = ('127.0.0.1',8712) #服务端绑定的地址和端口
server_socket = None #服务端socket
client_pool = [] #客户端连接池

#初始化
def init():
    global server_socket
    server_socket = socket.socket()
    server_socket.bind(addr)
    server_socket.listen(5)
    print('服务端已开启...')

#连接客户端
def acceptClient():
    while True:
        # 接收客户端请求
        client,a = server_socket.accept()
        #将新来的客户端连接加入连接池
        client_pool.append(client)
        thread = Thread(target=handleMessage,args=(client,a))
        thread.setDaemon(True) #设置成守护线程
        thread.start()

#消息处理
def handleMessage(client,a):
    #发送消息给客户端
    msg = '连接服务器成功！'
    client.sendall(msg.encode('utf-8'))
    while True:
        cmsg = client.recv(1024) #接收客户端消息
        print('客户端IP:{} 消息：{}'.format(a,cmsg))
        if len(cmsg)==0:
            client.close()
            #删除连接池中的连接
            client_pool.remove(client)
            print('客户端IP:{}已下线'.format(a))
            break

if __name__ == '__main__':
    init()
    #新开一个线程，用于接收新连接
    #acceptClient() 需要新开线程来打开连接客户端的函数，直接调用会阻塞，后面的主线程无法继续
    thread = Thread(target=acceptClient)
    thread.setDaemon(True) #设置成守护线程，主线程退出后子线程也跟着退出
    thread.start()

    #主线程
    while True:
        cmd = input("""--------------------------
        1:查看当前在线人数
        2:给指定客户端发送消息
        3:关闭服务端
        请输入：""")
        #输入的数字默认为字符串
        if cmd == '1':
            print('--------------------------')
            print('当前在线人数：{}'.format(len(client_pool)))
        if cmd == '2':
            print('--------------------------')
            index,msg = input('"请输入“索引,消息”的形式："').split(',')
            client_pool[int(index)].sendall(msg.encode('utf-8'))
        if cmd == '3':
            exit()

        #测试git使用
