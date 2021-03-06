# -*- coding: utf-8 -*-

"""AES encrypt decrypt."""

import hashlib
from Crypto import Random
from Crypto.Cipher import AES


class AESCipher():
    """Main class for AES cipher."""
    # pylint: disable=invalid-name

    def __init__(self, key):
        self.bs = 16
        self.key = hashlib.sha256(key.encode("utf8")).digest()
        self.turkish_converter = {'İ': '%10', 'ı': '%11', 'Ö': '%12',
                                  'ö': '%13', 'Ü': '%14', 'ü': '%15',
                                  'Ç': '%16', 'ç': '%17', 'Ğ': '%18',
                                  'ğ': '%19', 'Ş': '%20', 'ş': '%21'}

    def encrypt(self, raw):
        """Clear text to AES cipher method."""
        raw = self._turkish_character_encrypt(raw)
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        raw = self._character_control(raw).encode("utf8")
        return iv + cipher.encrypt(raw)

    def decrypt(self, enc):
        """AES cipher to clear text method."""
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decoded = self._unpad(cipher.decrypt(enc[AES.block_size:])).decode(
            'utf-8')
        return self._turkish_character_decrypt(decoded)

    def _turkish_character_encrypt(self, text):
        for i, j in self.turkish_converter.items():
            text = text.replace(i, j)
        return text

    def _turkish_character_decrypt(self, text):
        for i, j in self.turkish_converter.items():
            text = text.replace(j, i)
        return text

    def _character_control(self, text):  # noqa pylint: disable=no-self-use
        regular_text = ''
        for i in text:
            character = ord(i)
            if character > 127 or character < 0:
                character = 63
            regular_text += chr(character)
        return regular_text

    def _pad(self, text):
        return text + (self.bs - len(text) % self.bs) * chr(
            self.bs - len(text) % self.bs)

    @staticmethod
    def _unpad(text):
        return text[:-ord(text[len(text) - 1:])]
