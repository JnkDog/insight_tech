import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import time

class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # 解析 POST 数据
        parsed_data = parse_qs(post_data.decode('utf-8'))

        # 处理 POST 请求
        response_data = self.process_post_data(parsed_data)

        # 发送 JSON 响应 -- 分段传输了
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # 将字典序列化为 JSON 字符串
        response_json = json.dumps(response_data)
        self.wfile.write(response_json.encode('utf-8'))

    def process_post_data(self, data):
        # 在这里处理 POST 请求的数据
        # 这里只是一个简单的示例，你可以根据需要进行修改
        return {"status": "success", "data": data}

def run(server_class=HTTPServer, handler_class=MyHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
    # 获取当前时间戳
    # current_timestamp = time.time()
    # structured_time = time.localtime(current_timestamp)
    # milliseconds = int((current_timestamp - int(current_timestamp)) * 1000)
    # formatted_time = time.strftime("%Y-%m-%d %H:%M:%S.{:03d}", structured_time).format(milliseconds)
    # print("Current Time with Milliseconds:", formatted_time)
