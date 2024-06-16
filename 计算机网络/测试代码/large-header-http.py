from http.server import BaseHTTPRequestHandler, HTTPServer
import time

class CustomHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 创建一个大小为 1.5KB 的 HTTP 头
        response_headers = [
            ("Content-Type", "text/html"),
            ("Connection", "close"),
            ("Custom-Header", "A" * (1536 - len("HTTP/1.1 200 OK\r\n") - len("Content-Type: text/html\r\n") - len("Connection: close\r\n") - len("Custom-Header: ") - 4))
        ]

        time.sleep(15)
        # 发送响应状态码
        self.send_response(200)
        
        # 发送响应头
        for header in response_headers:
            self.send_header(header[0], header[1])
        self.end_headers()
        
        # 发送响应体
        self.wfile.write(b"Hello, world!")

def run(server_class=HTTPServer, handler_class=CustomHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
