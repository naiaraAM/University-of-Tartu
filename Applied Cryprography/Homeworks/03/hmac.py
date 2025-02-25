#!/usr/bin/env python3

import codecs, hashlib, sys
from pyasn1.codec.der import decoder
sys.path = sys.path[1:] # don't remove! otherwise the library import below will try to import your hmac.py
import hmac # do not use any other imports/libraries

# took 3.5 hours, maybe a little bit less, its appox

ALGORITHMS_OID = {
    'MD5': [1, 2, 840, 113549, 2, 5],
    'SHA1': [1, 3, 14, 3, 2, 26],
    'SHA256': [2, 16, 840, 1, 101, 3, 4, 2, 1],
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

#==== ASN1 encoder end ====

class DigestInfo:
    def __init__(self, filename, key, algorithm='SHA256'):
        self.filename = filename
        self.key = key.encode()  # Convert string to bytes
        self.algorithm = algorithm
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

def mac(filename):
    key = input("[?] Enter key: ")

    digest_info = DigestInfo(filename, key)
    hmac_digest = digest_info.encode()

    print("[+] Calculated HMAC-SHA256:", hmac_digest.hex())

    print("[+] Writing HMAC DigestInfo to", filename+".hmac")
    digest_info.write()

def verify(filename):
    print("[+] Reading HMAC DigestInfo from", filename + ".hmac")

    with open(filename + '.hmac', 'rb') as f:
        der_data = f.read()

    decoded = decoder.decode(der_data)[0]
    stored_digest = bytes(decoded[1])
    algorithm_oid = decoded[0][0]
    algorithm_oid_list = [int(x) for x in algorithm_oid]  # Convert to list of integers
    for key, value in ALGORITHMS_OID.items():
        if value == algorithm_oid_list:
            algorithm = key
            break
    print(f"[+] HMAC-{algorithm} digest: {stored_digest.hex()}")
    key = input("[?] Enter key: ")

    # print out the calculated HMAC-X digest
    digest_info = DigestInfo(filename, key, algorithm)
    calculated_digest = digest_info.encode()
    print(f"[+] Calculated HMAC-{algorithm}: {calculated_digest.hex()}")

    if calculated_digest != stored_digest:
        print("[-] Wrong key or message has been manipulated!")
    else:
        print("[+] HMAC verification successful!")



def usage():
    print("Usage:")
    print("-mac <filename>")
    print("-verify <filename>")
    sys.exit(1)

if len(sys.argv) != 3:
    usage()
elif sys.argv[1] == '-mac':
    mac(sys.argv[2])
elif sys.argv[1] == '-verify':
    verify(sys.argv[2])
else:
    usage()