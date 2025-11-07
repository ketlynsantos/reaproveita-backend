import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

from blog import get_all_posts
from contact import handle_contact


class ReaproveitaServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_header("Content-type", "application/json")
        self.send_header(
            "Access-Control-Allow-Origin", "https://reaproveita-react.vercel.app"
        )
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == "/blog":
            posts = get_all_posts()
            self.send_response(200)
            self._set_headers()
            self.end_headers()
            self.wfile.write(json.dumps(posts).encode())

        else:
            self.send_response(404)
            self._set_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "Rota nao encontrada"}')

    def do_POST(self):
        if self.path == "/contact":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))

            name = data.get("name")
            email = data.get("email")
            message = data.get("message")

            # Insere no banco (contato)
            handle_contact(name, email, message)

            self.send_response(200)
            self._set_headers()
            self.end_headers()
            response = {"status": "success", "message": "Mensagem enviada com sucesso!"}
            self.wfile.write(json.dumps(response).encode())

        else:
            self.send_response(404)
            self._set_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "Rota nao encontrada"}')


if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 8080))  # Render define a porta automaticamente
    server_address = ("", PORT)

    print(f"Servidor Reaproveita rodando na porta {PORT}")
    print("Rotas disponíveis:")
    print("/blog     (GET)     -> Retorna os posts do blog")
    print("/contact  (POST)    -> Envia formulário de contato")

    httpd = HTTPServer(server_address, ReaproveitaServer)
    httpd.serve_forever()
