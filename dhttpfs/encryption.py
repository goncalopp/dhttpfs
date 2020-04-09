from abc import ABC, abstractmethod
from pathlib import Path
import subprocess
import tempfile

class DecryptionError(Exception):
    pass

class Decryptor(ABC):
    def __init__(self, key):
        self.key = key

    @abstractmethod
    def decrypt(self, b):
        """Decrypts a byte buffer. Returns the unecrypted buffer or raises DecryptionError"""
        raise NotImplementedError

    @abstractmethod
    def extension(self):
        raise NotImplementedError

class GpgDecryptor(Decryptor):
    def decrypt(self, b):
        try:
            return gpg_decrypt(b, self.key)
        except Exception as e:
            raise DecryptionError from e

    def extension(self):
        return ".gpg"

def gpg_decrypt(data, passphrase):
    """decrypts binary (bytes) data using gpg symmetric encryption"""
    passphrase = passphrase.encode("utf-8")
    with tempfile.TemporaryDirectory() as directory:
        d = Path(directory)
        f1 = d / "encrypted"
        f2 = d / "decrypted"
        with f1.open("wb") as f:
            f.write(data)
        p = subprocess.Popen(["gpg", "--batch", "--decrypt", "--yes", "--passphrase-fd", "0", "--output", f2, f1], stdin=subprocess.PIPE, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        out_streams = p.communicate(passphrase)
        out = out_streams[0]
        if p.returncode != 0:
            raise Exception("GPG failed. Output: " + str(out))
        decrypted_data = f2.read_bytes()
        if len(decrypted_data) == 0:
            raise Exception("Unexpected empty file")
        return decrypted_data

