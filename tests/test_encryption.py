import unittest

from dhttpfs import encryption as tested

ENCRYPTED_CONTENT = b"""\x8c\r\x04\t\x03\x0242\xc4w\x99\x91\xb5\xee\xff\xd2D\x01\x89{\x87\xd7\x8eG97\xb5\x8a\xcf\xccp\x11\xd7~\x96p\xf7\xd9_K4\x85\x05nl\x18\xc6\x10\xe6O\xec\xd1\xc0-\xbd\x08_0O\xd4y\x92{\x9d\xef\x8d\x13\xde\xb7E\x82\xfe\x96.\x16r\xeb\x05\x8cO\x9d{i\xad\x7f"""
DECRYPTED_CONTENT = b"hello world\n"
KEY = "testpassword"

class GpgDecryptorTest(unittest.TestCase):
    def test_decrypt(self):
        d = tested.GpgDecryptor(KEY)
        result = d.decrypt(ENCRYPTED_CONTENT)
        self.assertEqual(result, DECRYPTED_CONTENT)

    def test_decrypt_wrongkey(self):
        d = tested.GpgDecryptor("wrongkey")
        with self.assertRaises(tested.DecryptionError):
            d.decrypt(ENCRYPTED_CONTENT)

    def test_decrypt_baddata(self):
        d = tested.GpgDecryptor(KEY)
        with self.assertRaises(tested.DecryptionError):
            d.decrypt(b"malformed data")

if __name__ == "__main__":
    unittest.main()
