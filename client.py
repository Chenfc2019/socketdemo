#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : client.py
# @Author: Small-orange
# @Date  : 2020-3-10
# @Desc  : 客户端，将数据上传到服务端

import socket
import time

c = socket.socket() #创建socket对象
c.connect(('127.0.0.1', 8712)) #连接的服务端的IP和端口
smsg = c.recv(1024).decode('utf-8')
print(smsg)

c.send('{} 客户端发来消息'.format(time.ctime()))
input("")