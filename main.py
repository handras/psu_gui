from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import json
from random import random
from urllib.parse import parse_qs

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):

    def serve_main(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(open('html/psu_gui.html').read(), "utf-8"))

    def serve_refresher(self):
        self.send_response(200)
        self.send_header("Content-type", "text/javascript")
        self.end_headers()
        self.wfile.write(bytes(open('scripts/refresher.js').read(), "utf-8"))

    def serve_setter(self):
        self.send_response(200)
        self.send_header("Content-type", "text/javascript")
        self.end_headers()
        self.wfile.write(bytes(open('scripts/setter.js').read(), "utf-8"))

    def serve_current(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            'ch1_volt_usage': 1.92 + random(),
            'ch1_amp_usage': 0.448 + random(),
            'ch2_volt_usage': 2.0005 + random(),
            'ch2_amp_usage': 3.24546 + random(),
        }
        ).encode('utf-8'))

    def serve_notfound(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    resources = {
        '/scripts/refresher.js': serve_refresher,
        '/scripts/setter.js': serve_setter,
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
        self.send_response_only(200)


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
