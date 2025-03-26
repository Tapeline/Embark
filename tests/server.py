import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Process
from pathlib import Path

import pytest


class _Server(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        """Handle GET."""
        try:
            path = os.path.join("tests\\fixtures", self.path[1:])
            data = Path(path).read_text()
            self.send_response(200)
        except FileNotFoundError:
            data = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(data, "utf-8"))


def _run_server():
    httpd = HTTPServer(("localhost", 8080), _Server)
    httpd.serve_forever()


def _run_server_in_separate_proc():
    proc = Process(target=_run_server, args=())
    proc.start()
    return proc


@pytest.fixture(scope="function")
def serve_fixture_files():
    """Serve files located in tests/fixtures."""
    proc = _run_server_in_separate_proc()
    try:
        yield
    finally:
        while proc.is_alive():
            proc.terminate()
