from Crypto.Cipher import Blowfish
import math
import binascii

class Blowfisher(object):

    def __init__(self, secret):
        self.secret = secret

    def _break(self, data, n):
        limit = int(math.ceil(len(data)/float(n)))
        return [data[i*n:(i+1)*n] for i in range(limit)]

    def decode(self, token):
    
        blowfish = Blowfish.new(self.secret)
        iv = '00' * 8
    
        token_split = self._break(token, 2)
        token_split = self._break(token_split, 8)
            
        secret_string = []
        count = 0
        for chunk in token_split:
            count += 1
            iv = ''.join([chr(int(h, 16)) for h in self._break(iv, 2)])
            iv = blowfish.encrypt(iv)
            iv = ''.join(['%0.2x' % ord(c) for c in iv])
            ivs = self._break(iv, 2)
                
            strings = [chr(ord(binascii.unhexlify(c)) ^ int(i, 16)) for c, i in zip(chunk, ivs)]
            secret_string.append(''.join(strings))
            iv = token[16 * (count-1):16+(16 * (count-1))]
    
        return ''.join(secret_string)


    def encode(self, text):

        blowfish = Blowfish.new(self.secret)
        iv = '00' * 8
        token = ''

        for block in self._break(text, 8):
            iv = ''.join([chr(int(h, 16)) for h in self._break(iv, 2)])
            iv = blowfish.encrypt(iv)
            iv = ''.join(['%0.2x' % ord(c) for c in iv])
            ivs = self._break(iv, 2)
    
            chars = ['%0.2x' % (ord(c) ^ int(i, 16)) for c, i in zip(block, ivs)]
            token += ''.join(chars)
            iv = ''.join(chars)
        return token
