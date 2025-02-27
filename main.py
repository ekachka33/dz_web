from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

# Настройки сервера
hostName = "localhost"
serverPort = 8080

# Ссылка на удалённый репозиторий с шаблоном
REMOTE_TEMPLATE_URL = "https://raw.githubusercontent.com/user/repository/main/contacts.html"

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        """Обрабатывает любой GET-запрос и возвращает страницу 'Контакты'"""
        try:
            response = requests.get(REMOTE_TEMPLATE_URL)
            response.raise_for_status()
            content = response.text
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(content, "utf-8"))
        except requests.RequestException:
            self.send_response(500)
            self.end_headers()
            self.wfile.write("Ошибка загрузки страницы".encode('utf-8'))

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Сервер запущен на http://{hostName}:{serverPort}")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Сервер остановлен")
