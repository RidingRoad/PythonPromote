import socket, re

from mini_web_server_response import *

from multiprocessing import Process

'''
实现MiniWebServer 的大体流程
1.http是基于tcp 协议的,那么根据tcp创建相应的套接字以接收请求和响应
2.对客户端请求的处理: 通过对请求行的分析获取客户端请求的资源
3.回应请求:对请求进行分类,读取相关资源后根据http协议的要求进行封装返回给客户端.
4.使用多进程实现多任务多个同时访问的能力
'''


def handler_client(cli_socket):
    # 连接后返回连接请求内容
    request_content = cli_socket.recv(1024).decode()
    # 提取请求数据
    request_line = request_content.splitlines()[0]
    regex = re.compile(r"\w+ +/([^ ]*) ")
    try:
        request_resource = regex.match(request_line).group(1)
        print(request_resource)

        # 如果后面没跟数据,就返回主页
        if request_resource == '':
            cli_socket.send(index())
            cli_socket.close()
        else:
            # 存在返回相应的资源或不存在返回404
            cli_socket.send(other_file(request_resource))
            cli_socket.close()
    except Exception as e:
        print("error in regular expression")
        cli_socket.close()


def main():
    # 创建服务器套接字
    server_socket = socket.socket()  # 默认family=AF_INET, type=SOCK_STREAM,即tcp协议的套接字

    # 套接字复用
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    # 给服务器绑定ip地址和端口号
    server_socket.bind(("", 9999))

    # 把服务器状态改为监听模式
    server_socket.listen(1024)

    while True:
        # 等待客户端的连接并返回一个专为客户端服务用的套接字
        cli_socket, cli_addr = server_socket.accept()
        print(cli_addr)
        cli_socket_process = Process(target=handler_client,args=(cli_socket,))
        cli_socket_process.start()
        cli_socket.close()

if __name__ == '__main__':
    main()
