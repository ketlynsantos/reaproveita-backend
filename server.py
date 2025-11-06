import http.server
import json
from socketserver import TCPServer
from urllib.parse import parse_qs

from blog import get_all_posts
from contact import handle_contact


class ReaproveitaServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/blog":
            posts = get_all_posts()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(posts).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/contact":
            length = int(self.headers["Content-Length"])
            body = self.rfile.read(length).decode()
            data = parse_qs(body)
            name = data.get("name", [""])[0]
            email = data.get("email", [""])[0]
            message = data.get("message", [""])[0]

            handle_contact(name, email, message)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {"status": "ok", "message": "Contact sent successfully"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    with TCPServer(("", 8081), ReaproveitaServer) as httpd:
        print("Reaproveita backend running at http://localhost:8081")
        # Mantém o servidor rodando até ser interrompido
        httpd.serve_forever()
