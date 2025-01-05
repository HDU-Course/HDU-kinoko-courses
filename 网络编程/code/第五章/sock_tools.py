# -*- coding: utf-8 -*-
"""
sock工具库

@author: zhangzhen
"""

#####################################################
# 常用的socket 读写函数
def sock_readline(sock):
    line = b''
    data = b''
    while (data != b'\n'):
        data = sock.recv(1)
        if (data == b''):
            break
        line += data
    return line

def sock_readn(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            return data
        data += more
    return data

def sock_writeline(sock, data):
    sock.send(data)
    sock.send(b'\n')

def sock_writen(sock, data, length):
    if (len(data) > length):
        sock.send(data[0:length])
    else:
        sock.send(data)

def sock_write(sock, data):
    sock.send(data)

############################################################
# 提供带buffer缓存的sock读写函数，减少socket函数调用次数，提高效率

def sock_buf_readline(sock, data_buf=b''):
    data_list = []
    index = -1
    data = b''
    if (data_buf != b''):
        data = data_buf
        index = data.find(b'\n')
    
    while (index == -1):
        if (data != b''):
            data_list.append(data)
        
        data = sock.recv(4096)
        if (data == b''):
            break
        
        index = data.find(b'\n')
    
    if (data == b''):
        return (b''.join(data_list), b'')
    
    data_list.append(data[0:index+1])
    return (b''.join(data_list), data[index+1:])

def sock_buf_readn(sock, length, data_buf=b''):
    data_list = []
    
    data = data_buf
    index = len(data_buf)
    while (index < length):
        if (data != b''):
            data_list.append(data)
        
        data = sock.recv(4096)
        if (data == b''):
            break
        
        index += len(data)
    
    if (data == b''):
        return (b''.join(data_list), b'')
    
    index = len(data) - (length - index)
    data_list.append(data[0:index])
    return (b''.join(data_list), data[index:])

def sock_buf_read(sock, data_buf=b''):
    if (len(data_buf) > 0):
        return data_buf
       
    return sock.recv(4096)

