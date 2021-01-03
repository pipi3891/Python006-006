#!/usr/bin/env python
import socket
import os
import hashlib

HOST = 'localhost'
PORT = 10000


def echo_server():
    ''' Echo Server 的 Server 端 '''

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 对象s绑定到指定的主机和端口上
    s.bind((HOST, PORT))
    # 只接受1个连接
    s.listen(1)
    while True:
        # accept表示接受用户端的连接
        conn, addr = s.accept()
        # 输出客户端地址
        print(f'Connected by {addr}')
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
        conn.close()
    s.close()

def send_file():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 对象s绑定到指定的主机和端口上
    s.bind((HOST, PORT))
    # 只接受1个连接
    s.listen(1)
    while True:
        conn, addr = s.accept()
        print(f'Connected by {addr}')
        while True:
            data = conn.recv(1024)
            print(data)
            if not data:
                print("客户端已断开")
                break
            cmd, fileName = data.decode().split()

            if os.path.isfile(fileName):
                f = open(fileName, "rb")
                print(f)
                m = hashlib.md5()
                print(m)
                # 获取文件大小
                file_size = os.stat(fileName).st_size
                print("filesize:",file_size)

                # 向客户端发送文件大小
                conn.sendall(str(file_size).encode())
                # wait for ack
                conn.recv(1024)

                for line in f:
                    # 获取md5
                    m.update(line)
                    # 发送数据
                    conn.send(line)

                print("file md5:", m.hexdigest())
                conn.send(m.hexdigest().encode())
                f.close()
            else:
                print("文件不存在！")
                msg = "文件不存在"
                conn.sendall(msg.encode())
        conn.close()
    s.close()


if __name__ == '__main__':
    # echo_server()
    send_file()