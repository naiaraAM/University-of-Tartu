#!/usr/bin/env python3
import sys

def ib(i):  # based on previous HW
    b = b''
    while i > 0:
        b = bytes([i & 0xFF]) + b
        i >>= 8
    return b

def bi(b):  # based on previous HW
    i = 0 # initialize var
    for _ in range(len(b)):
        i = i << 8
        i = i | b[_]
    return i


class  DERencoder:
    def __init__(self):
        return

    def asn1_boolean(self, boolean):
        type_byte = bytes([0x01])
        output = b''
        if boolean:
            output = bytes([0xFF])
        else:
            output = bytes([0x00])
        length = self.asn1_len(output)
        return type_byte + length + output

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

    def asn1_bitstring(self, bitstr):
        type_byte = bytes([0x03])
        nbits = len(bitstr)
        unused_bits = (8 - (nbits % 8)) % 8
        val = 0
        for bit in bitstr:
            val = (val << 1) | (1 if bit == '1' else 0)
        val <<= unused_bits

        required_bytes = (nbits + 7) // 8
        value_bytes = bytes([unused_bits])

        if nbits > 0:
            val_bytes = ib(val)
            padding = b'\x00' * (required_bytes - len(val_bytes))
            value_bytes += padding + val_bytes

        length = self.asn1_len(value_bytes)
        return type_byte + length + value_bytes

    def asn1_octetstring(self, bytes_in):
        type_byte = bytes([0x04])
        # Convert hex string to bytes
        if isinstance(bytes_in, str):
            bytes_in = bytes.fromhex(bytes_in.replace(" ", ""))
        length = self.asn1_len(bytes_in)
        return type_byte + length + bytes_in

    def asn1_null(self):
        type_byte = bytes([0x05])
        length = bytes([0x00])
        return type_byte + length

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

    def asn1_sequence(self, der):
        type_byte = bytes([0x30])
        length = self.asn1_len(der)
        return type_byte + length + der

    def asn1_set(self, der):
        type_byte = bytes([0x31])
        length = self.asn1_len(der)
        return type_byte + length + der

    def asn1_utf8string(self, utf8bytes):
        type_byte = bytes([0x0C])
        value_bytes = utf8bytes if isinstance(utf8bytes, bytes) else utf8bytes.encode('utf-8')  # Avoid mismatches
        length = self.asn1_len(value_bytes)
        return type_byte + length + value_bytes

    def asn1_utctime(self, time):
        type_byte = bytes([0x17])
        value_bytes = time.encode('ascii')
        length = self.asn1_len(value_bytes)
        return type_byte + length + value_bytes

    def asn1_tag_explicit(self, der, tag):
        if not 0 <= tag <= 30:  # Check boundaries
            print("Tag value not in boundaries")
            sys.exit(-1)
        type_byte = bytes([0x80 | 0x20 | tag])
        length = self.asn1_len(der)
        return type_byte + length + der

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


if __name__ == "__main__":
    # Check number of arguments
    if len(sys.argv) != 2:
        print("Usage: asn1_encoder.py <output_file>")
        sys.exit(1)

    encoder = DERencoder()
    asn1 = encoder.asn1_tag_explicit(
        encoder.asn1_sequence(
            encoder.asn1_set(
                encoder.asn1_integer(5) +
                encoder.asn1_tag_explicit(
                    encoder.asn1_integer(200),
                    2
                ) +
                encoder.asn1_tag_explicit(
                    encoder.asn1_integer(65407),
                    11
                )
            ) +
            encoder.asn1_boolean(True) +
            encoder.asn1_bitstring('011') +
            encoder.asn1_octetstring('00 01 02 02 02 02 02 02 02 02 02 02 02 02 02 02'
                                     '02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02'
                                     '02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02'
                                     '02 02 02') +
            encoder.asn1_null() +
            encoder.asn1_objectidentifier([1, 2, 840, 113549, 1]) +
            encoder.asn1_utf8string('hello.') +
            encoder.asn1_utctime('250227010900Z')
        ),
        0
    )
    open(sys.argv[1], 'wb').write(asn1)
