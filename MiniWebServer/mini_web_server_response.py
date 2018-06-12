import os


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
        response_header = "Content-Type:text/html\r\n"
        response = response_line + response_header + "\r\n"
        return response.encode()+data
    else:
        response_line = "HTTP/1.1 404 NOT FOUND\r\n"
        response_header = "Content-Type:text/html\r\n"
        response = response_line + response_header + "\r\n" + "404 FILE NOT FOUND"
        return (response.encode())
