from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import json
from random import random
from urllib.parse import parse_qs
from pathlib import Path

try:
    from pyci2.core.psu_api import PSU
except:
    pass

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):

    try:
        p = PSU()
    except:
        pass

    def serve_file(self):
        if Path(self.path[1:]).exists():
            self.send_response(200)
            self.send_header("Content-type", "text/javascript")
            self.send_header("cache-control", "public, max-age=352800")
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
        try:
            self.wfile.write(json.dumps(self.p.readback_status).encode('utf-8'))
        except:
            self.wfile.write(json.dumps({
                'ch1_state': '0',
                'ch1_volt_usage': f'{24.92 + random():05.2f}',
                'ch1_amp_usage' : f'{0.148 + random():05.2f}',
                'ch2_state': '1',
                'ch2_volt_usage': f'{2.004 + random():05.2f}',
                'ch2_amp_usage' : f'{3.246 + random():05.2f}',
            }
            ).encode('utf-8'))

    def serve_notfound(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _set_channel(self, data):

        def clean(data):
            return round(float(data[0]),2)

        if data.get(b'ch1_volt'):
            # print(f'set ch1 v to {clean(data[b"ch1_volt"])}, i to {clean(data[b"ch1_current"])}')
            self.p.turn_on(1, clean(data[b"ch1_volt"]), data[b"ch1_current"])
        else:
            # print(f'set ch2 v to {clean(data[b"ch2_volt"])}, i to {clean(data[b"ch2_current"])}')
            self.p.turn_on(2, clean(data[b"ch2_volt"]), data[b"ch2_current"])

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
        if self.path == '/set.json':
            # print('set.json in do_POST:' + str(data))
            self._set_channel(data)
        if self.path == '/setOff.json':
            # print(f'turning off: {int(data[b"ch"][0])}')
            self.p.turn_off(int(data[b"ch"][0]))
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
