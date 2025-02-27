import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import os

logging.basicConfig(level=logging.DEBUG)

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/':
                # Обработка главной страницы
                response = requests.get("https://raw.githubusercontent.com/ekachka33/dz_web/7cac1a973acb95fea3d91ff528a210e734b487a8/contact.html")
                response.raise_for_status()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(response.text.encode('utf-8'))
            elif self.path == '/favicon.ico':
                # Обработка favicon.ico
                if os.path.exists("favicon.ico"):
                    self.send_response(200)
                    self.send_header("Content-type", "image/x-icon")
                    self.end_headers()
                    with open("favicon.ico", "rb") as f:
                        self.wfile.write(f.read())
                else:
                    self.send_response(404)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write("favicon.ico не найден.".encode('utf-8'))
            else:
                # Для других путей
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write("Страница не найдена.".encode('utf-8'))
        except Exception as e:
            logging.error(f"Ошибка при обработке запроса: {e}")
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f"Произошла ошибка: {str(e)}".encode('utf-8'))

def run():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, MyHandler)
    logging.info('Сервер запущен на http://localhost:8080')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
