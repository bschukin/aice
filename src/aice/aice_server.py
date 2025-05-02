from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from src.aice.aice_service2 import generate_command

class SimpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/aice'):
            try:
                parsed_url = urlparse(self.path)
                query_params = parse_qs(parsed_url.query)

                input_string = query_params.get('query', [''])[0]
                res = generate_command(input_string)

                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')  # Меняем на text/plain
                self.end_headers()
                self.wfile.write(res.encode('utf-8'))  # Просто пишем строку
            except Exception as e:
                # Логируем ошибку (можно добавить запись в лог-файл)
                print(f"Ошибка при генерации команды: {str(e)}")

                # Отправляем клиенту сообщение об ошибке
                self.send_response(500)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(f"Ошибка при обработке запроса: {str(e)}".encode('utf-8'))
        else:
            self.send_error(404, "Страница не найдена")


if __name__ == '__main__':
    server_address = ('', 8888)
    httpd = HTTPServer(server_address, SimpleServer)
    print("Сервер запущен на порту 8888")
    httpd.serve_forever()
