#!/usr/bin/env python3

import codecs, hashlib, os, sys # do not use any other imports/libraries
from secp256r1 import curve
from pyasn1.codec.der import decoder

def ib(i, length=False):
    # converts integer to bytes
    b = b''
    if length==False:
        length = (i.bit_length()+7)//8
    for _ in range(length):
        b = bytes([i & 0xff]) + b
        i >>= 8
    return b

def bi(b):
    # converts bytes to integer
    i = 0
    for char in b:
        i <<= 8
        i |= char
    return i

# --------------- asn1 DER encoder
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
    if i == 0:
        output = b'\x00'
    if (output[0] & 0x80) != 0:
        output = b'\x00' + output
    length = asn1_len(output)
    return type_byte + length + output

def signature(r, s):
    return asn1_sequence(
        asn1_integer(r) +
        asn1_integer(s)
    )
# --------------- asn1 DER encoder end


def pem_to_der(content):
    # converts PEM content (if it is PEM) to DER
    if content[:2] == b'--':
        content = content.replace(b"-----BEGIN PUBLIC KEY-----", b"")
        content = content.replace(b"-----END PUBLIC KEY-----", b"")
        content = content.replace(b"-----BEGIN PRIVATE KEY-----", b"")
        content = content.replace(b"-----END PRIVATE KEY-----", b"")
        content = codecs.decode(content, 'base64')
    return content

def get_privkey(filename):
    # reads EC private key file and returns the private key integer (d)
    key_file_pem = open(filename, 'rb').read()
    key_file_der = pem_to_der(key_file_pem)

    key_file_der, _ = decoder.decode(key_file_der)
    octet_string_encapsulated = key_file_der[2]

    private_key_der, _ = decoder.decode(octet_string_encapsulated)

    d = bi(private_key_der[1])
    return d

def get_pubkey(filename):
    # reads EC public key file and returns coordinates (x, y) of the public key point
    key_file_pem = open(filename, 'rb').read()
    key_file_der = pem_to_der(key_file_pem)

    key_file_der, _ = decoder.decode(key_file_der)

    bit_string = key_file_der[1]
    point_bytes = bit_string.asOctets()
    control_byte = point_bytes[0]
    if control_byte != 0x04:
        sys.exit(-1)
    x = bi(point_bytes[1:33])
    y = bi(point_bytes[33:65])
    return x, y

def ecdsa_sign(keyfile, filetosign, signaturefile):
    # get the private key
    d = get_privkey(keyfile)

    # calculate SHA-384 hash of the file to be signed
    sha384_file = hashlib.sha384(open(filetosign, 'rb').read()).digest()

    # Convert hash to integer and truncate to the bit length of curve.n
    h = bi(sha384_file) >> 128
    h %= curve.n

    # Rest of the function remains the same...
    while True:
        # Generate random nonce k
        while True:
            random_nonce = os.urandom(32)
            k = bi(random_nonce)
            if 0 < k < curve.n:
                break

        # Calculate signature components
        random_point = curve.mul(curve.g, k)
        r = random_point[0] % curve.n
        k_inverse = pow(k, -1, curve.n)
        # s = (k_inverse * ((h + (r * d) % curve.n) % curve.n)) % curve.n
        s = (k_inverse * (h + r * d)) % curve.n

        if r != 0 and s != 0:
            break

    signature_der = signature(r, s)
    with open(signaturefile, 'wb') as f:
        f.write(signature_der)
    return r, s


def ecdsa_verify(keyfile, signaturefile, filetoverify):
    # Get the public key
    pub_key = get_pubkey(keyfile)

    with open(signaturefile, 'rb') as f:
        signature_der = f.read()

    signature_der, _ = decoder.decode(signature_der)

    r = int(signature_der.getComponentByPosition(0))
    s = int(signature_der.getComponentByPosition(1))

    # Verify r and s are in range [1, n-1]
    if r not in range(1, curve.n) or s not in range(1, curve.n):
        print("Verification failure")
        sys.exit(-1)

    # Calculate hash with the SAME truncation logic as in signing
    file_data = open(filetoverify, 'rb').read()
    hash_digest = hashlib.sha384(file_data).digest()

    # Convert hash to integer and apply the same truncation used in signing
    h = bi(hash_digest) >> 128
    h %= curve.n

    # Verification formula
    s_inverse = pow(s, -1, curve.n)
    u1 = (h * s_inverse) % curve.n
    u2 = (r * s_inverse) % curve.n

    point_1 = curve.mul(curve.g, u1)
    point_2 = curve.mul(pub_key, u2)
    R_aux = curve.add(point_1, point_2)

    r_aux_modulo_n = R_aux[0] % curve.n

    if r_aux_modulo_n == r:
        print("Verified OK")
    else:
        print("Verification failure")

def usage():
    print("Usage:")
    print("sign <private key file> <file to sign> <signature output file>")
    print("verify <public key file> <signature file> <file to verify>")
    sys.exit(1)

if len(sys.argv) != 5:
    usage()
elif sys.argv[1] == 'sign':
    ecdsa_sign(sys.argv[2], sys.argv[3], sys.argv[4])
elif sys.argv[1] == 'verify':
    ecdsa_verify(sys.argv[2], sys.argv[3], sys.argv[4])
else:
    usage()