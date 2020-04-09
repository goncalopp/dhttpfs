from http import HTTPStatus
import http.server
import logging
from io import BytesIO as StringIO
import os
from pathlib import Path
import urllib

import dhttpfs.encryption as encryption

log = logging.getLogger(__name__)


class Handler(http.server.BaseHTTPRequestHandler):


    def do_GET(self):
        helper_class = http.server.SimpleHTTPRequestHandler
        fake_helper = Exception()
        fake_helper.directory = str(self.server.directory)

        path = helper_class.translate_path(fake_helper, self.path)
        # support getting the file with a missing encryption file extension
        d_ext = self.server.decryptor.extension()
        p1, p2 = Path(path), Path(path + d_ext)
        path = p2 if p2.exists() else p1
        if not path.is_file():
            if path.is_dir():
                # Directory listing not allowed
                log.warning("Directory listing not allowed")
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None
        encrypted = path.read_bytes()
        try:
            decrypted = self.server.decryptor.decrypt(encrypted)
        except encryption.DecryptionError as e:
            log.exception(e)
            self.send_error(HTTPStatus.UNPROCESSABLE_ENTITY, "A decrytion failure occurred")
            return None
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "application/octet-stream")
        self.send_header("Content-Length", str(len(decrypted)))
        self.end_headers()
        self.wfile.write(decrypted)


class Server(http.server.HTTPServer):
    def __init__(self, server_address, key, directory=None, handler_class=Handler):
        super().__init__(server_address, handler_class)
        self.directory = Path(directory or os.getcwd())
        self.decryptor = encryption.GpgDecryptor(key)

    def serve_forever(self, *args, **kwargs):
        host, port = self.server_address
        log.info("Running server on %s:%s", host, port)
        super().serve_forever(*args, **kwargs)

if __name__ == "__main__":
    import argparse
    import getpass

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('--bind', '-b', default='localhost', help='bind address '
                             '[default: localhost only]')
    parser.add_argument('--directory', '-d', default=os.getcwd())
    parser.add_argument('port', action='store', default=8000, type=int, nargs='?',
                        help='port [default: 8000]')
    args = parser.parse_args()

    # WARNING: do NOT modify this code to accept passwords as an argument
    # https://stackoverflow.com/questions/3830823/hiding-secret-from-command-line-parameter-on-unix
    # https://serverfault.com/questions/592744/how-to-hide-a-password-passed-as-command-line-argument
    password = getpass.getpass("Password:")

    addr = (args.bind, args.port)
    server = Server(addr, "testpassword", args.directory)
    server.serve_forever()

