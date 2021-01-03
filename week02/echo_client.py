#!/usr/bin/env python
import socket
import hashlib


HOST = 'localhost'
PORT = 10000


def echo_client():
    ''' Echo Server 的 Client 端 '''

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    while True:
        # 接收用户输入数据并发送服务端
        data = input('input > ')

        # 设定退出条件
        if data == 'exit':
            break

        # 发送数据到服务端
        s.sendall(data.encode())

        # 接收服务端数据
        data = s.recv(1024)
        if not data:
            break
        else:
            print(data.decode('utf-8'))

    s.close()

def recv_file():
    '''
    接受服务器文件
    :return:
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    while True:
        cmd = input(">>:").strip()
        if len(cmd) == 0: continue
        if cmd.startswith("exit"):
            break
        if cmd.startswith("get"):
            s.send(cmd.encode())
            # 接收文件大小
            server_response = s.recv(1024)
            print(server_response.decode())
            if server_response.decode()=='文件不存在':
                continue
            else:
                print("文件大小：", server_response.decode())

                # 发送确认
                s.send(b"ok")

                file_size = int(server_response.decode())
                received_size = 0
                filename = cmd.split()[1]
                f = open(filename + ".new", "wb")
                m = hashlib.md5()
                #     received_data = b""
                while received_size < file_size:
                    buff = 0;
                    # 只收取文件中的字符
                    if file_size - received_size > 1024:
                        buff = 1024
                    else:
                        buff = file_size - received_size
                        # 接收数据
                    cmd_res = s.recv(buff)
                    # 每次收到的字节数
                    received_size = received_size + len(cmd_res)

                    m.update(cmd_res)
                    # 将接收的数据写到文件中
                    f.write(cmd_res)
                else:
                    print("done")
                    f.close()
                    new_file_md5 = m.hexdigest()

                server_file_md5 = s.recv(1024)
                print("server md5 is :", server_file_md5)
                print("client md5 is :", new_file_md5)
    s.close()


if __name__ == '__main__':
    # echo_client()
    recv_file()