#!/usr/bin/env python3

import time, os, sys
from pyasn1.codec.der import decoder

# $ sudo apt-get install python3-pycryptodome
sys.path = sys.path[1:] # removes current directory from aes.py search path
from Cryptodome.Cipher import AES          # https://pycryptodome.readthedocs.io/en/latest/src/cipher/classic.html#ecb-mode
from Cryptodome.Util.strxor import strxor  # https://pycryptodome.readthedocs.io/en/latest/src/util/util.html#crypto-util-strxor-module
from hashlib import pbkdf2_hmac
import hashlib, hmac # do not use any other imports/libraries

# took 2.5 hours (please specify here how much time your solution required)

ALGORITHMS_OID = {
    'md5': [1, 2, 840, 113549, 2, 5],
    'sha1': [1, 3, 14, 3, 2, 26],
    'sha256': [2, 16, 840, 1, 101, 3, 4, 2, 1],
    'aes128-CBC': [2, 16, 840, 1, 101, 3, 4, 1, 2],
}

#==== ASN1 encoder start ====
# put your DER encoder functions here
class ASN1_encoder:
    def ib(self, i):  # based on previous HW
        b = b''
        while i > 0:
            b = bytes([i & 0xFF]) + b
            i >>= 8
        return b

    def asn1_objectidentifier(self, oid):
        type_byte = bytes([0x06])

        first = 40 * oid[0] + oid[1]
        output = bytes([first])

        for comp in oid[2:]:
            bits = []
            temp = comp
            bits.append(temp & 0x7F)
            temp >>= 7
            while temp:
                bits.append(temp & 0x7F)
                temp >>= 7

            for i in range(len(bits) - 1, 0, -1):
                output += bytes([bits[i] | 0x80])
            output += bytes([bits[0]])

        length = self.asn1_len(output)
        return type_byte + length + output

    def asn1_len(self, value_bytes):
        length_value = len(value_bytes)
        if length_value < 128:
            return bytes([length_value])
        needed_bytes = 0
        temp = length_value
        while temp > 0:
            temp >>= 8
            needed_bytes += 1
        first_byte = 0x80 | needed_bytes
        return bytes([first_byte]) + self.ib(length_value)

    def asn1_sequence(self, der):
        type_byte = bytes([0x30])
        length = self.asn1_len(der)
        return type_byte + length + der

    def asn1_null(self):
        type_byte = bytes([0x05])
        length = bytes([0x00])
        return type_byte + length

    def asn1_octetstring(self, bytes_in):
        type_byte = bytes([0x04])
        # Convert hex string to bytes
        if isinstance(bytes_in, str):
            bytes_in = bytes.fromhex(bytes_in.replace(" ", ""))
        length = self.asn1_len(bytes_in)
        return type_byte + length + bytes_in

    def asn1_integer(self, i):
        if i < 0:
            print("Error: Only positive integers supported")
            sys.exit(-1)
        type_byte = bytes([0x02])
        output = self.ib(i)
        if i == 0:
            output = b'\x00'
        if (output[0] & 0x80) != 0:
            output = b'\x00' + output
        length = self.asn1_len(output)
        return type_byte + length + output

#==== ASN1 encoder end ====

class AES_info:
    def __init__(self, salt, iteration_count, algorithm, iv, pbkdf2_params, aes_info, filename, key, key_length=48):
        self.salt = salt
        self.iteration_count = iteration_count
        self.key_length = key_length
        self.algorithm = algorithm
        self.iv = iv
        self.pbkdf2_params = pbkdf2_params
        self.aes_info = aes_info
        self.encoder = ASN1_encoder()
        self.digest_info = DigestInfo(filename, key)

    def pbkdf2Params_encoder(self):
        return self.encoder.asn1_sequence(
                    self.encoder.asn1_octetstring(self.salt) +
                    self.encoder.asn1_integer(self.iteration_count) +
                    self.encoder.asn1_integer(self.key_length)
        )
    def aesInfo_encoder(self):
        oid = ALGORITHMS_OID['aes128-CBC']
        return self.encoder.asn1_sequence(
                    self.encoder.asn1_objectidentifier(oid) +
                    self.encoder.asn1_octetstring(self.iv)
        )
    def digestInfo_encoder(self):
        return self.digest_info.to_asn1()

    def encInfo_encoder(self):
        return self.encoder.asn1_sequence(
                    self.pbkdf2Params_encoder() +
                    self.aesInfo_encoder() +
                    self.digestInfo_encoder()
        )

class DigestInfo:
    def __init__(self, filename, key, algorithm='SHA256'):
        self.filename = filename
        self.key = key.encode()  # Convert string to bytes
        self.algorithm = algorithm.lower()
        self.asn1_encoder = ASN1_encoder()

    def encode(self):
        hash_function = getattr(hashlib, self.algorithm.lower())
        hmac_obj = hmac.new(self.key, None, hash_function)
        with open(self.filename, 'rb') as file:
            while chunk := file.read(512):
                hmac_obj.update(chunk)
            return hmac_obj.digest()

    def to_asn1(self):
        digest = self.encode()
        digest_der = self.asn1_encoder.asn1_sequence(
            self.asn1_encoder.asn1_sequence(
                self.asn1_encoder.asn1_objectidentifier(ALGORITHMS_OID[self.algorithm]) +
                self.asn1_encoder.asn1_null()
            ) +
            self.asn1_encoder.asn1_octetstring(digest)
        )
        return digest_der

    def write(self):
        asn1_representation = self.to_asn1()
        with open(self.filename + '.hmac', 'wb') as file:
            file.write(asn1_representation)


# this function benchmarks how many PBKDF2 iterations
# can be performed in one second on the machine it is executed
def benchmark():

    # measure time for performing 10000 iterations

    # extrapolate to 1 second
    start = time.time()
    hashlib.pbkdf2_hmac('sha1', b'password', b'salt', 10000)
    end = time.time()

    elapsed = end - start
    iters = int(10000 / elapsed)

    print("[+] Benchmark: %s PBKDF2 iterations in 1 second" % iters)

    return iters # returns number of iterations that can be performed in 1 second

def encrypt(pfile, cfile):

    # benchmarking
    num_iters = benchmark()

    # asking for a password
    password = input("[+] Enter password: ")
    if len(password) < 1:
        print("[!] Password cannot be empty")
        sys.exit(1)

    # deriving keys
    salt = os.urandom(8) # 64 bits
    key = pbkdf2_hmac('sha1', password.encode(), salt, num_iters, 48)

    aes_128_key = key[:16]
    hmac_sha256_key = key[16:]

    # reading plaintext
    plaintext = open(pfile, 'rb').read()

    # padding plaintext
    pad = 16 - (len(plaintext) % 16)
    plaintext += bytes([pad]) * pad

    # encrypting padded plaintext
    cipher = AES.new(aes_128_key, AES.MODE_ECB)
    iv = os.urandom(16)
    iv_current = iv
    ciphertext = b''

    for i in range(0, len(plaintext), 16):
        plaintext_block = plaintext[i:i+16]
        xor = strxor(plaintext_block, iv_current)
        encrypted_block = cipher.encrypt(xor)
        ciphertext += encrypted_block
        iv_current = encrypted_block

    # MAC calculation (iv+ciphertext)
    mac = hmac.new(hmac_sha256_key, iv+ciphertext, hashlib.sha256).digest()

    # constructing DER header
    aes_info = AES_info(salt, num_iters, 'SHA256', iv, key, ciphertext, pfile, password)
    der_header = aes_info.encInfo_encoder()

    # writing DER header and ciphertext to file
    f = open(cfile, 'wb')
    f.write(der_header)
    f.write(ciphertext)
    f.write(mac)
    f.close()

    pass

def decrypt(cfile, pfile):
    # reading DER header and ciphertext
    f = open(cfile, 'rb')
    contents = f.read()
    der_header, rest = decoder.decode(contents)
    f.close()

    # split the rest into IV, ciphertext, and MAC
    iv = der_header[1][1].asOctets()
    ciphertext = rest[:-32]  # Everything except last 32 bytes
    mac_from_file = rest[-32:]  # Last 32 bytes are MAC

    # asking for a password
    password = input("[+] Enter password: ")
    if len(password) < 1:
        print("[!] Password cannot be empty")
        sys.exit(1)

    # deriving keys
    salt = der_header[0][0].asOctets()
    iteration_count = int(der_header[0][1])
    dklen = int(der_header[0][2])
    key = pbkdf2_hmac('sha1', password.encode(), salt, iteration_count, dklen)

    aes_128_key = key[:16]
    hmac_sha256_key = key[16:]

    # Verify MAC (iv+ciphertext)
    mac_calculated = hmac.new(hmac_sha256_key, iv + ciphertext, hashlib.sha256).digest()
    if mac_from_file != mac_calculated:
        print("[-] HMAC verification failure: wrong password or modified ciphertext!")
        sys.exit(1)

    # decrypting ciphertext
    cipher = AES.new(aes_128_key, AES.MODE_ECB)
    iv_current = iv
    plaintext = b''

    for i in range(0, len(ciphertext), 16):
        ciphertext_block = ciphertext[i:i + 16]
        decrypted_block = cipher.decrypt(ciphertext_block)
        plaintext += strxor(decrypted_block, iv_current)
        iv_current = ciphertext_block

    # removing padding
    pad = plaintext[-1]
    if pad > 16 or pad < 1:
        print("[!] Invalid padding")
        sys.exit(1)

    # Verify padding
    if not all(x == pad for x in plaintext[-pad:]):
        print("[!] Invalid padding")
        sys.exit(1)

    plaintext = plaintext[:-pad]

    # writing plaintext to file
    with open(pfile, 'wb') as file:
        file.write(plaintext)

def usage():
    print("Usage:")
    print("-encrypt <plaintextfile> <ciphertextfile>")
    print("-decrypt <ciphertextfile> <plaintextfile>")
    sys.exit(1)


if len(sys.argv) != 4:
    usage()
elif sys.argv[1] == '-encrypt':
    encrypt(sys.argv[2], sys.argv[3])
elif sys.argv[1] == '-decrypt':
    decrypt(sys.argv[2], sys.argv[3])
else:
    usage()