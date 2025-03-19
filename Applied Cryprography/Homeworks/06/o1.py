#!/usr/bin/env python3

import codecs, hashlib, os, sys # do not use any other imports/libraries
from secp256r1 import curve
from pyasn1.codec.der import decoder

def ib(i, length=False):
    # Converts integer to bytes
    b = b''
    if length == False:
        length = (i.bit_length() + 7) // 8
    for _ in range(length):
        b = bytes([i & 0xff]) + b
    i >>= 8
    return b

def bi(b):
    # Converts bytes to integer
    i = 0
    for char in b:
        i = (i << 8) | char
    return i


def asn1_len(value_bytes):
    length_value = len(value_bytes)
    if length_value < 128:
        return bytes([length_value])
    needed_bytes = 0
    temp = length_value
    while temp > 0:
        temp >>= 8
        needed_bytes += 1
        first_byte = 0x80 | needed_bytes
        return bytes([first_byte]) + ib(length_value)

def asn1_sequence(der):
    type_byte = bytes([0x30])
    length = asn1_len(der)
    return type_byte + length + der

def asn1_integer(i):
    if i < 0:
        print("Error: Only positive integers supported")
        sys.exit(-1)
    type_byte = bytes([0x02])
    output = ib(i)
    # If integer is 0, we must encode it as single 0x00
    if i == 0:
    output = b'\x00'
    # If high bit is set, prepend 0x00 to keep it positive
    if (output[0] & 0x80) != 0:
    output = b'\x00' + output
    length = asn1_len(output)
    return type_byte + length + output

def signature(r, s):
return asn1_sequence(
asn1_integer(r) +
asn1_integer(s)
)
--------------------------------------------------------------------
ASN.1 DER encoder end

def pem_to_der(content):
# Converts PEM content (if it is PEM) to DER
if content[:2] == b'--':
content = content.replace(b"-----BEGIN PUBLIC KEY-----", b"")
content = content.replace(b"-----END PUBLIC KEY-----", b"")
content = content.replace(b"-----BEGIN PRIVATE KEY-----", b"")
content = content.replace(b"-----END PRIVATE KEY-----", b"")
content = codecs.decode(content, 'base64')
return content

def get_privkey(filename):
# Reads EC private key file and returns the private key integer d
key_file_pem = open(filename, 'rb').read()
key_file_der = pem_to_der(key_file_pem)

# Decode the DER structure

key_file_der, _ = decoder.decode(key_file_der)

# For an EC private key (Public Key Cryptography Standards #8),

# the actual private key octet string is at index 2

octet_string_encapsulated = key_file_der[2]


private_key_der, _ = decoder.decode(octet_string_encapsulated)

# The private key itself is at index 1 in that structure

d = bi(private_key_der[1])

return d

def get_pubkey(filename):
# Reads EC public key file and returns (x, y) coordinates of the public key point
key_file_pem = open(filename, 'rb').read()
key_file_der = pem_to_der(key_file_pem)

# Decode the DER structure

key_file_der, _ = decoder.decode(key_file_der)


# For a SubjectPublicKeyInfo structure, the BIT STRING is at index 1

bit_string = key_file_der[1]

# Convert BIT STRING to octets, which start with control_byte

point_bytes = bit_string.asOctets()

control_byte = point_bytes[0]

if control_byte != 0x04:

    print("Error: Uncompressed EC point expected (0x04).")

    sys.exit(-1)


# Next 32 bytes are x, next 32 bytes are y (for secp256r1)

x = bi(point_bytes[1:33])

y = bi(point_bytes[33:65])

return x, y

def ecdsa_sign(keyfile, filetosign, signaturefile):
# 1. Get the private key
d = get_privkey(keyfile)

# 2. Calculate the SHA-384 hash of the file to be signed

file_data = open(filetosign, 'rb').read()

sha384_file = hashlib.sha384(file_data).digest()


# 3. Truncate the hash value to the curve size

#    This is effectively done by taking it mod curve.n

h = bi(sha384_file) % curve.n


# 4. Generate a random nonce k in [1, n-1]

#    (For security, use RFC 6979 if you want deterministic k)

while True:

    random_nonce = os.urandom(32)  # 32 bytes => 256 bits

    k = bi(random_nonce)

    if 0 < k < curve.n:

        break


# 5. Calculate r = R.x mod n, where R = k × G

random_point = curve.mul(curve.g, k)

r = random_point[0] % curve.n


# 6. Calculate k_inverse = k^(-1) mod n

k_inverse = pow(k, -1, curve.n)


# 7. Calculate s = k_inverse * (h + r*d) mod n

s = (k_inverse * (h + r * d)) % curve.n


# 8. DER-encode (r, s) and save to file

signature_der = signature(r, s)

with open(signaturefile, 'wb') as f:

    f.write(signature_der)


return r, s

def ecdsa_verify(keyfile, signaturefile, filetoverify):
# 1. Extract public key Q = (x, y)
pub_key = get_pubkey(keyfile)

# 2. Read and parse signature DER

with open(signaturefile, 'rb') as f:

    signature_der = f.read()

signature_decoded, _ = decoder.decode(signature_der)


# r and s are the two INTEGERs in the SEQUENCE

r = int(signature_decoded[0])

s = int(signature_decoded[1])


# Basic range checks

if not (1 <= r < curve.n) or not (1 <= s < curve.n):

    print("Verification failure: r or s out of range")

    sys.exit(-1)


# 3. Compute hash of message to verify

file_data = open(filetoverify, 'rb').read()

sha384_file = hashlib.sha384(file_data).digest()

h = bi(sha384_file) % curve.n


# 4. Compute s_inverse = s^(-1) mod n

s_inverse = pow(s, -1, curve.n)


# 5. Compute u1 = h * s_inverse mod n

#           u2 = r * s_inverse mod n

u1 = (h * s_inverse) % curve.n

u2 = (r * s_inverse) % curve.n


# 6. Compute R′ = u1 × G + u2 × Q

point_1 = curve.mul(curve.g, u1)

point_2 = curve.mul(pub_key, u2)

R_aux = curve.add(point_1, point_2)


# 7. Verification: R′.x mod n == r ?

if (R_aux[0] % curve.n) == r:

    print("Verified OK")

else:

    print("Verification failure")

def usage():
print("Usage:")
print(" sign ")
print(" verify ")
sys.exit(1)
if len(sys.argv) != 5:
usage()
elif sys.argv[1] == 'sign':
ecdsa_sign(sys.argv[2], sys.argv[3], sys.argv[4])
elif sys.argv[1] == 'verify':
ecdsa_verify(sys.argv[2], sys.argv[3], sys.argv[4])
else:
usage()