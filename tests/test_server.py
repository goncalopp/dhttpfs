import http.client
from pathlib import Path
import tempfile
import threading
import unittest

from dhttpfs import server as tested

ENCRYPTED_CONTENT = b"""\x8c\r\x04\t\x03\x0242\xc4w\x99\x91\xb5\xee\xff\xd2D\x01\x89{\x87\xd7\x8eG97\xb5\x8a\xcf\xccp\x11\xd7~\x96p\xf7\xd9_K4\x85\x05nl\x18\xc6\x10\xe6O\xec\xd1\xc0-\xbd\x08_0O\xd4y\x92{\x9d\xef\x8d\x13\xde\xb7E\x82\xfe\x96.\x16r\xeb\x05\x8cO\x9d{i\xad\x7f"""
DECRYPTED_CONTENT = b"hello world\n"
KEY = "testpassword"
FILENAME = "myfile"

class ServerThread(threading.Thread):
    def __init__(self, directory, start_event):
        threading.Thread.__init__(self)
        self.host = "" # assigned later
        self.port = 0 # assigned later
        self.directory = directory
        self.start_event = start_event

    def run(self):
        self.server = tested.Server(('localhost', 0), KEY, str(self.directory))
        self.host, self.port = self.server.socket.getsockname()
        self.start_event.set()
        try:
            self.server.serve_forever(0.5) # poll_interval
        finally:
            self.server.server_close()

    def stop(self):
        self.server.shutdown()
        self.join()

class ServerTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        server_started = threading.Event()
        self.thread = ServerThread(self.tempdir, server_started)
        self.thread.start()
        server_started.wait()
        self.host, self.port = self.thread.host, self.thread.port
        self.directory = Path(self.tempdir)

    def tearDown(self):
        try:
            shutil.rmtree(self.tempdir)
        except:
            pass
        finally:
            self.thread.stop()
            self.thread = None

    def _request(self, url, method='GET', body=None, headers={}):
        conn = http.client.HTTPConnection(self.host, self.port)
        conn.request(method, url, body, headers)
        return conn.getresponse()

    def test_get_dir(self):
        res = self._request("/")
        self.assertEqual(res.status, 404)

    def test_get_inexistent(self):
        res = self._request("/" + FILENAME)
        self.assertEqual(res.status, 404)

    def test_get_unencrypted(self):
        (self.directory / FILENAME).write_bytes(b"randomdata")
        res = self._request("/" + FILENAME)
        self.assertEqual(res.status, 422)

    def test_get_encrypted(self):
        (self.directory / FILENAME).write_bytes(ENCRYPTED_CONTENT)
        res = self._request("/" + FILENAME)
        self.assertEqual(res.status, 200)
        self.assertEqual(res.read(), DECRYPTED_CONTENT)


if __name__ == "__main__":
    unittest.main()
