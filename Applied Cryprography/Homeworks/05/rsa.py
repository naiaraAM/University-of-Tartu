#!/usr/bin/env python3

import codecs, hashlib, os, sys # do not use any other imports/libraries

from pyasn1.codec.der import decoder

# took x.y hours (please specify here how much time your solution required)


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
    for byte in b:
        i <<= 8
        i |= byte
    return i

#==== ASN1 encoder start ====
# put your DER encoder functions here
class DER_encoder:
    def __init__(self, filetosign):
        self.filetosign = filetosign
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
        return bytes([first_byte]) + ib(length_value)

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
        output = ib(i)
        if i == 0:
            output = b'\x00'
        if (output[0] & 0x80) != 0:
            output = b'\x00' + output
        length = self.asn1_len(output)
        return type_byte + length + output

    def digest_info(self):
        alorithm_identifier = self.asn1_sequence(
            self.asn1_objectidentifier([2, 16, 840, 1, 101, 3, 4, 2, 1]) +
            self.asn1_null()
        )
        with open(self.filetosign, 'rb') as f:
            plainfile = f.read()
        digest = hashlib.sha256(plainfile).digest()
        return self.asn1_sequence(alorithm_identifier + self.asn1_octetstring(digest))

def rsa_encryption_private():
    """
    OBJECT IDENTIFIER ::= { iso(1) member-body(2) us(840) rsadsi(113549) pkcs(1) pkcs-1(1) 1 }
    """

def algorithm_identifier_private_key():
    """
    AlgorithmIdentifier  ::=  SEQUENCE  {
        algorithm               OBJECT IDENTIFIER :== rsa_encryption,
        parameters              ANY DEFINED BY algorithm OPTIONAL ::= NULL
    }
    """
    pass

def rsa_private_key():
    """
    RSAPrivateKey ::= SEQUENCE {
        version           INTEGER,  -- 0 for two-prime RSA
        modulus           INTEGER,  -- n
        publicExponent    INTEGER,  -- e
        privateExponent   INTEGER,  -- d
        prime1            INTEGER,  -- p
        prime2            INTEGER,  -- q
        exponent1         INTEGER,  -- d mod (p-1)
        exponent2         INTEGER,  -- d mod (q-1)
        coefficient       INTEGER,  -- (inverse of q) mod p
        otherPrimeInfos   OtherPrimeInfos OPTIONAL
    }
    """
    pass

def private_key_info():
    """
    PrivateKeyInfo ::= SEQUENCE {
        version                   INTEGER,
        privateKeyAlgorithm       AlgorithmIdentifier,
        privateKey                OCTET STRING ::= RSAPrivateKey,
        attributes           [0]  IMPLICIT Attributes OPTIONAL
    }
    """
    pass

def rsa_encryption_public():
    """
    OBJECT IDENTIFIER ::= { iso(1) member-body(2) us(840) rsadsi(113549) pkcs(1) pkcs-1(1) 1 }
    """

def algorithm_identifier_public_key():
    """
    AlgorithmIdentifier  ::=  SEQUENCE  {
        algorithm               OBJECT IDENTIFIER :== rsa_encryption,
        parameters              ANY DEFINED BY algorithm OPTIONAL ::= NULL
    }
    """
    pass

def rsa_public_key():
    """
    RSAPublicKey ::= SEQUENCE {
        modulus           INTEGER,  -- n
        publicExponent    INTEGER   -- e
    }
    """
    pass

def subject_public_key_info():
    """
    SubjectPublicKeyInfo  ::=  SEQUENCE  {
        algorithm            AlgorithmIdentifier,
        subjectPublicKey     BIT STRING ::= RSAPublicKey
    }
    """
    pass



#==== ASN1 encoder end ====

def pem_to_der(content):
    # converts PEM content to DER
    if b'-----BEGIN ' not in content: # already DER
        return content

    start = content.find(b'-----BEGIN ')
    end = content.find(b'-----END ')

    if start != -1 and end != -1:
        start = content.find(b'\n', start) + 1
        base64_data  = b''.join(content[start:end].split())
        der = codecs.decode(base64_data, 'base64')
        return der

def get_pubkey(filename):
    # reads public key file encoded using SubjectPublicKeyInfo structure and returns (N, e)
    with open(filename, 'rb') as f:
        content = f.read()
    der_data = pem_to_der(content)

    subject_public_key_info, _ = decoder.decode(der_data)

    # DER-decode the DER to get RSAPublicKey DER structure, which is encoded as BITSTRING
    bit_string_rsa = subject_public_key_info.getComponentByPosition(1)

    # convert BITSTRING to bytestring
    rsa_pub_der = bit_string_rsa.asOctets()

    # DER-decode the bytestring (which is actually DER) and return (N, e)
    rsa_pub, _ = decoder.decode(rsa_pub_der)
    modulus = int(rsa_pub.getComponentByPosition(0))
    public_exponent = int(rsa_pub.getComponentByPosition(1))

    return modulus, public_exponent

def get_privkey(filename):
    # reads private key file encoded using PrivateKeyInfo (PKCS#8) structure and returns (N, d)
    with open(filename, 'rb') as f:
        content = f.read()
    der_data = pem_to_der(content)

    private_key_info, _ = decoder.decode(der_data)

    # DER-decode the DER to get RSAPrivateKey DER structure, which is encoded as OCTETSTRING
    rsa_private_key_octet = private_key_info.getComponentByPosition(2)

    # DER-decode the octetstring (which is actually DER) and return (N, d)
    rsa_private_key, _ = decoder.decode(rsa_private_key_octet)
    modulus = int(rsa_private_key.getComponentByPosition(1))
    private_exponent = int(rsa_private_key.getComponentByPosition(3))

    return modulus, private_exponent


def pkcsv15pad_encrypt(plaintext, n):
    # pad plaintext for encryption according to PKCS#1 v1.5
    # calculate number of bytes required to represent the modulus N
    k = (n.bit_length() + 7) // 8

    # plaintext must be at least 11 bytes smaller than the modulus
    if len(plaintext) > k - 11:
        print("[!] Plaintext is too long for encryption")
        sys.exit(1)

    # generate padding bytes
    ps_len = k - len(plaintext) - 3
    ps = b''
    while len(ps) < ps_len:
        byte = os.urandom(1)
        if byte != b'\x00':
            ps += byte

    padded_plaintext = b'\x00\x02' + ps + b'\x00' + plaintext

    return padded_plaintext

def pkcsv15pad_sign(plaintext, n):
    # pad plaintext for signing according to PKCS#1 v1.5

    # calculate bytelength of modulus N
    byte_length = (n.bit_length() + 7) // 8

    # plaintext must be at least 11 bytes smaller than the modulus N
    if len(plaintext) > byte_length - 11:
        print("[!] Plaintext is too long for signing")
        sys.exit(1)
    # PS (padding string) – 8 or more 0xFF bytes
    padding_string = b'\xff' * (byte_length - len(plaintext) - 3)

    # generate padding bytes
    return b'\x00\x01' + padding_string + b'\x00' + plaintext

def pkcsv15pad_remove(plaintext, mode='decrypt'):
    # removes PKCS#1 v1.5 padding
    if mode == 'decrypt':
        if plaintext[0:2] != b'\x00\x02':
            print("[!] Invalid padding")
            sys.exit(1)

        # padding is between 0x00 0x02 and 0x00
        i = 2
        while plaintext[i] != 0:
            i += 1
        i += 1

        return plaintext[i:]
    elif mode == 'verify':
        if len(plaintext) < 3 or plaintext[0:2] != b'\x00\x01':
            print("[!] Invalid padding")
            return None

        # Find the end of padding (0xFF bytes followed by 0x00)
        i = 2
        while i < len(plaintext) and plaintext[i] == 0xFF:
            i += 1

        # Ensure we found the 0x00 separator after the padding
        if i >= len(plaintext) or plaintext[i] != 0:
            print("[!] Invalid padding")
            return None

        # Skip the 0x00 separator
        i += 1
        return plaintext[i:]

    return None

def encrypt(keyfile, plaintextfile, ciphertextfile):
    # Obtain modulus and public exponent from public key file
    modulus, public_exponent = get_pubkey(keyfile)

    with open(plaintextfile, 'rb') as f:
        plaintext = f.read()

    # Apply padding
    padded_plaintext = pkcsv15pad_encrypt(plaintext, modulus)

    int_padded_plaintext = bi(padded_plaintext)

    # Create ciphertext
    ciphertext = ib(pow(int_padded_plaintext, public_exponent, modulus))

    # Save ciphertext to file
    with open(ciphertextfile, 'wb') as f:
        f.write(ciphertext)

    print(f"[+] Encrypted plaintext and saved to {ciphertextfile}")

def decrypt(keyfile, ciphertextfile, plaintextfile):
    # Obtain modulus and private exponent from private key file
    modulus, private_exponent = get_privkey(keyfile)
    modulus_bytes = (modulus.bit_length() + 7) // 8 # calculate bytelength of modulus N

    with open(ciphertextfile, 'rb') as f:
        ciphertext = f.read()

    int_ciphertext = bi(ciphertext)

    # Obtain plaintext padded
    int_padded_plaintext = pow(int_ciphertext, private_exponent, modulus)

    byte_padded_plaintext = ib(int_padded_plaintext, modulus_bytes) # convert to bytes

    # Remove padding
    plaintext = pkcsv15pad_remove(byte_padded_plaintext, 'decrypt')

    # Save to file
    with open(plaintextfile, 'wb') as f:
        f.write(plaintext)

    print(f"[+] Decrypted plaintext saved to {plaintextfile}")
    pass

def sign(keyfile, filetosign, signaturefile):
    modulus, private_exponent = get_privkey(keyfile)
    modulus_bytes = (modulus.bit_length() + 7) // 8
    encoder = DER_encoder(filetosign)
    plaintext = encoder.digest_info()

    padded_plaintext = pkcsv15pad_sign(plaintext, modulus)
    int_padded_plaintext = bi(padded_plaintext)

    signature = pow(int_padded_plaintext, private_exponent, modulus)
    signature_bytes = ib(signature, modulus_bytes)

    with open(signaturefile, 'wb') as f:
        f.write(signature_bytes)
    print(f"[+] Signature saved to {signaturefile}")


def verify(keyfile, signaturefile, filetoverify):
    # prints "Verified OK" or "Verification failure"
    with open(signaturefile, 'rb') as f:
        signature = f.read()
    modulus, public_exponent = get_pubkey(keyfile)
    modulus_bytes = (modulus.bit_length() + 7) // 8  # Calculate byte length of modulus

    int_signature = bi(signature)
    int_decrypted = pow(int_signature, public_exponent, modulus)

    # Convert to bytes with exact modulus length
    decrypted_bytes = ib(int_decrypted, modulus_bytes)

    # Use the existing function to remove padding with 'verify' mode
    no_padding_signature = pkcsv15pad_remove(decrypted_bytes, 'verify')

    # Generate fresh DigestInfo from file
    encoder = DER_encoder(filetoverify)
    digestinfo_from_file = encoder.digest_info()

    if no_padding_signature == digestinfo_from_file:
        print("Verified OK")
    else:
        print("Verification failure")

def usage():
    print("Usage:")
    print("encrypt <public key file> <plaintext file> <output ciphertext file>")
    print("decrypt <private key file> <ciphertext file> <output plaintext file>")
    print("sign <private key file> <file to sign> <signature output file>")
    print("verify <public key file> <signature file> <file to verify>")
    sys.exit(1)

if len(sys.argv) != 5:
    usage()
elif sys.argv[1] == 'encrypt':
    encrypt(sys.argv[2], sys.argv[3], sys.argv[4])
elif sys.argv[1] == 'decrypt':
    decrypt(sys.argv[2], sys.argv[3], sys.argv[4])
elif sys.argv[1] == 'sign':
    sign(sys.argv[2], sys.argv[3], sys.argv[4])
elif sys.argv[1] == 'verify':
    verify(sys.argv[2], sys.argv[3], sys.argv[4])
else:
    usage()