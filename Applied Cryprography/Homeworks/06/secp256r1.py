#!/usr/bin/env python3

def bi(b):
    # converts bytes to integer
    i = 0
    for byte in b:
        i <<= 8
        i |= byte
    return i

def ib(i, length=32):
    # converts integer to bytes
    b = b''
    if length==False:
        length = (i.bit_length()+7)//8
    for _ in range(length):
        b = bytes([i & 0xff]) + b
        i >>= 8
    return b

# curve implementation in python
class Curve:

    def __init__(self):
        # curve parameters for NIST P-256 (ANSI prime256v1, SECG secp256r1)
        # https://www.nsa.gov/ia/_files/nist-routines.pdf
        # http://perso.univ-rennes1.fr/sylvain.duquesne/master/standards/sec2_final.pdf
        self.p = 2**256-2**224+2**192+2**96-1
        self.a = self.p-3
        self.b = 41058363725152142129326129780047268409114441015993725554835256314039467401291
        gx = bi(bytes.fromhex("6b17d1f2 e12c4247 f8bce6e5 63a440f2 77037d81 2deb33a0 f4a13945 d898c296".replace(' ', '')))
        gy = bi(bytes.fromhex("4fe342e2 fe1a7f9b 8ee7eb4a 7c0f9e16 2bce3357 6b315ece cbb64068 37bf51f5".replace(' ', '')))
        self.g = [gx,gy]
        self.n = 115792089210356248762697446949407573529996955224135760342422259061068512044369

    def valid(self,point):
        xP = point[0]

        if xP==None:
            return False

        yP = point[1]
        return yP**2 % self.p == (pow(xP, 3, self.p) + self.a*xP + self.b) % self.p

    def decompress(self,compressed):
        byte = compressed[0:1]

        # point at infinity
        if byte==b"\x00":
            return [None,None]

        xP = bi(compressed[1:])
        ysqr = (pow(xP, 3, self.p) + self.a*xP + self.b) % self.p
        assert self.p % 4 == 3
        yP = pow(ysqr, (self.p + 1) // 4, self.p)
        assert pow(yP, 2, self.p)==ysqr
        if yP % 2:
            if byte==b"\x03":
                return [xP,yP]
            return [xP, -yP % self.p]
        if byte==b"\x02":
            return [xP,yP]
        return [xP, -yP % self.p]

    def compress(self,P):

        if P[0] == None:
            return b"\x00" + b"\x00"*32

        byte = b"\x02"
        if P[1] % 2:
            byte = b"\x03"
        return byte + ib(P[0])

    def inv(self,point):
        xP = point[0]

        if xP==None:
            return [None,None]

        yP = point[1]
        R = [xP,-yP % self.p]
        return R

    def add(self,P,Q):

        # P+P=2P
        if P==Q:
            return self.dbl(P)

        # P+0=P
        if P[0]==None:
            return Q
        if Q[0]==None:
            return P

        # P+-P=0
        if Q==self.inv(P):
            return [None,None]

        xP = P[0]
        yP = P[1]
        xQ = Q[0]
        yQ = Q[1]
        s = (yP - yQ) * pow(xP - xQ, -1, self.p) % self.p
        xR = (pow(s,2,self.p) - xP -xQ) % self.p
        yR = (-yP + s*(xP-xR)) % self.p
        R = [int(xR),int(yR)]
        return R

    def dbl(self,P):
        # 2*0=0
        if P[0]==None:
            return P

        # yP==0
        if P[1]==0:
            return [None,None]

        xP = P[0]
        yP = P[1]
        s = (3*pow(xP,2,self.p)+self.a) * pow(2*yP,-1,self.p) % self.p
        xR = (pow(s,2,self.p) - 2*xP) % self.p
        yR = (-yP + s*(xP-xR)) % self.p
        R = [int(xR),int(yR)]
        return R

    def mul(self, P, k):
        # x0=0
        if P[0]==None:
            return P

        N = P
        R = [None,None]

        while k:
            bit = k % 2
            k >>= 1
            if bit:
                R = self.add(R,N)
            N = self.dbl(N)

        if R[0]==None:
            return R

        return [int(R[0]),int(R[1])]

curve = Curve()