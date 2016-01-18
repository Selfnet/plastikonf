from Crypto.Cipher import DES
from hashlib import md5
import sys

key = b'\x47\x8D\xA5\x0B\xF9\xE3\xD2\xCF'
crypto = DES.new( key, DES.MODE_ECB )
fi = open(sys.argv[1], "rb").read()
dec = crypto.decrypt(fi)[16:].rstrip(b"\0")
print(dec.decode())
