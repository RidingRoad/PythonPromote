import os, re


def handler_client(cli_socket):
    # 连接后返回连接请求内容
    request_content = cli_socket.recv(1024).decode()
    # 提取请求数据
    request_line = request_content.splitlines()[0]
    regex = re.compile(r"\w+ +/([^ ]*) ")
    try:
        request_resource = regex.match(request_line).group(1)

        # 如果后面没跟数据,就返回主页
        if '' == request_resource:
            cli_socket.send(index())
            cli_socket.close()
        else:
            # 存在返回相应的资源或不存在返回404
            cli_socket.send(other_file(request_resource))
            cli_socket.close()
    except Exception as e:
        print("error in regular expression")
        cli_socket.close()


def index():
    response_line = "HTTP/1.1 200 OK\r\n"
    response_header = "Content-Type:text/html\r\n"
    # 读取首页内容
    with open('index.html', 'r') as index_file:
        index_data = index_file.read()
    response = response_line + response_header + "\r\n" + index_data
    return response.encode()


def other_file(file_name):
    file_list = os.listdir("static/")
    if file_name in file_list:
        # 读取内容
        with open("static/" + file_name, 'rb') as request_file:
            data = request_file.read()

            response_line = "HTTP/1.1 200 OK\r\n"
            response_header = "Content-Type:image/jpg\r\n"
            # response_header = "Content-Type:text/html\r\n"
            response = response_line + response_header + "\r\n"
            return response.encode() + data

    else:
        response_line = "HTTP/1.1 404 NOT FOUND\r\n"
        response_header = "Content-Type:text/html\r\n"
        response = response_line + response_header + "\r\n" + "404 FILE NOT FOUND"
        return (response.encode())
