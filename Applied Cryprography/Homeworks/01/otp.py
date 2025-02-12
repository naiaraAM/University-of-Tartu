#!/usr/bin/env python3
import os, sys       # do not use any other imports/libraries

# took 2 hours


def bi(b):
    # b - bytes to encode as an integer
    # your implementation here

    i = 0 # initialize var
    for _ in range(len(b)):
        i = i << 8
        i = i | b[_]
    return i

def ib(i, length):
    # i - an integer to encode as bytes
    # length - specifies in how many bytes the integer should be encoded
    # your implementation here
    b = b''
    for _ in range(length):
        b = bytes([i & 0xFF]) + b
        i >>= 8
    return b

def encrypt(pfile, kfile, cfile): #  assume that pfile is in execution directory
    # your implementation here

    # read plaintext
    file_bytes = open(pfile, 'rb').read()

    # convert to bytes to one big string integer
    file_integer = bi(file_bytes)

    # obtain random key, use os.urandom(size)
    random_key = os.urandom(len(file_bytes))

    # convert key bytes to one big integer
    key_integer = bi(random_key)

    # perform XOR
    ciphertext_integer = file_integer ^ key_integer

    # save key and ciphertext (convert before to bytes)
    key_bytes = ib(key_integer, len(file_bytes))
    ciphertext_bytes = ib(ciphertext_integer, len(file_bytes))

    binary_key_file = open(kfile, "wb")
    binary_key_file.write(key_bytes)
    binary_key_file.close()

    binary_ciphertext_file = open(cfile, "wb")
    binary_ciphertext_file.write(ciphertext_bytes)
    binary_ciphertext_file.close()
    pass

def decrypt(cfile, kfile, pfile):
    # your implementation here

    # read bytes from cfile and kfile
    ciphertext_bytes = open(cfile, 'rb').read()
    key_bytes = open(kfile, 'rb').read()

    # convert to integer
    ciphertext_integer = bi(ciphertext_bytes)
    key_integer = bi(key_bytes)

    # perform xor
    plain_xor = ciphertext_integer ^ key_integer

    # convert xor to bytes
    plain_bytes = ib(plain_xor, len(ciphertext_bytes))

    # write plain_bytes to file
    binary_plain_file = open(pfile, "wb")
    binary_plain_file.write(plain_bytes)
    binary_plain_file.close()

    pass

def usage():
    print("Usage:")
    print("encrypt <plaintext file> <output key file> <ciphertext output file>")
    print("decrypt <ciphertext file> <key file> <plaintext output file>")
    sys.exit(1)

if len(sys.argv) != 5:
    usage()
elif sys.argv[1] == 'encrypt':
    encrypt(sys.argv[2], sys.argv[3], sys.argv[4]) # assume that all arguments are passed correctly
elif sys.argv[1] == 'decrypt':
    decrypt(sys.argv[2], sys.argv[3], sys.argv[4]) # assume that all arguments are passed correctly
else:
    usage()
