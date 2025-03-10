import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Process

import pytest


class Server(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        try:
            path = os.path.join("tests\\fixtures", self.path[1:])
            with open(path) as req_f:
                data = req_f.read()
            self.send_response(200)
        except FileNotFoundError:
            data = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(data, "utf-8"))


def run_server():
    httpd = HTTPServer(("localhost", 8080), Server)
    httpd.serve_forever()


def run_server_in_separate_proc():
    proc = Process(target=run_server, args=())
    proc.start()
    return proc


@pytest.fixture(scope="function")
def serve_fixture_files():
    proc = run_server_in_separate_proc()
    try:
        yield
    finally:
        while proc.is_alive():
            proc.terminate()
