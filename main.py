from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import json
from random import random
from urllib.parse import parse_qs
from pathlib import Path

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):

    def serve_file(self):
        if Path(self.path[1:]).exists():
            self.send_response(200)
            self.send_header("Content-type", "text/javascript")
            self.end_headers()
            self.wfile.write(bytes(open(self.path[1:]).read(), "utf-8"))
        else:
            self.serve_notfound()

    def serve_main(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(open('html/psu_gui.html').read(), "utf-8"))

    def serve_current(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            'ch1_volt_usage': f'{24.92 + random():05.2f}',
            'ch1_amp_usage' : f'{0.148 + random():05.2f}',
            'ch2_volt_usage': f'{2.004 + random():05.2f}',
            'ch2_amp_usage' : f'{3.246 + random():05.2f}',
        }
        ).encode('utf-8'))

    def serve_notfound(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    resources = {
        '/scripts/refresher.js': serve_file,
        '/scripts/setter.js': serve_file,
        '/scripts/my_displays.js': serve_file,
        '/scripts/segment-display.js': serve_file,
        '/current.json': serve_current,
        '/': serve_main,
    }

    def do_GET(self):
        try:
            self.resources.get(self.path, None)(self)
        except TypeError as e:
            self.serve_notfound()

    def parse_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse_qs(
                self.rfile.read(length),
                keep_blank_values=True)
        else:
            postvars = {}
        return postvars

    def do_POST(self):
        data = self.parse_POST()
        print('in do_POST:' + str(data))
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b'ok')


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
