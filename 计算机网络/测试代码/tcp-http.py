import socket
import json
import time

def send_json_post_request(host, port, path, headers, json_data):
    # 将 JSON 数据转换为字符串
    data_str = json.dumps(json_data)

    # 构建 HTTP 请求
    request_header = f"POST {path} HTTP/1.1\r\n" \
              f"Host: {host}\r\n" \
              f"{headers}\r\n" \
              "Content-Type: application/json\r\n" \
              f"Content-Length: {len(data_str)}\r\n" \
              "\r\n" \

    request_body = f"{data_str}"

    # 创建 TCP 套接字
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 连接到服务器
        s.connect((host, port))

        # 发送 HTTP 请求
        s.sendall(request_header.encode())
        print_cur_time('before 0.2s ')
        time.sleep(2)
        s.sendall(request_body.encode())
        print_cur_time('after')
        #40948 53846
        # 接收服务器响应
        response = s.recv(1024)

    print("Server response:")
    print(response.decode())

def print_cur_time(show_str):
    print(f"======== {show_str} =======")
    current_timestamp = time.time()
    structured_time = time.localtime(current_timestamp)
    milliseconds = int((current_timestamp - int(current_timestamp)) * 1000)
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S.{:03d}", structured_time).format(milliseconds)
    print("Current Time with Milliseconds:", formatted_time)



if __name__ == "__main__":
    # 设置服务器的主机、端口和路径
    server_host = "localhost"
    server_port = 80
    server_path = "/upstream"

    # 设置 JSON 格式的数据
    json_data = {"key1": "value1", "key2": "value2"}

    # 设置自定义的请求头
    custom_headers = "Authorization: Bearer Token123"

    # 发送 JSON 格式的 POST 请求
    send_json_post_request(server_host, server_port, server_path, custom_headers, json_data)
