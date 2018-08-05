import urllib2
import sys

TARGET = 'http://crypto-class.appspot.com/po?er='
CIPHER_TEXT = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c" + \
    "001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"
AES_BLOCK_SIZE = 16

def xor(*blocks):
    return ''.join([chr(reduce(lambda x, y: x ^ ord(y), b, 0)) for b in zip(*blocks)])

#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):

    # All ASCII char in preferred order
    # a-z, A-Z, space-@, remaining ascii char
    GUESS_ORDER = range(97, 123) + range(65, 91) + range(32, 65) + \
                  range(0, 32) + range(91, 97) + range(123, 256)

    def query(self, q):
        target = TARGET + urllib2.quote(q)    # Create query URL
        req = urllib2.Request(target)         # Send HTTP request to server
        try:
            f = urllib2.urlopen(req)          # Wait for response
        except urllib2.HTTPError, e:
            # print "We got: %d" % e.code       # Print response code
            if e.code == 404:
                return True # good padding
            return False # bad padding

    def _attempt_func(self, blocks, i):
        pre = ''.join(blocks[:i])
        return lambda pad, mbg: pre + xor(blocks[i], pad, mbg) + blocks[i+1]

    def cipher_text_guess(self, hex_cipher_text):
        cipher_text = hex_cipher_text.decode("hex")
        blocks = [cipher_text[b:b+AES_BLOCK_SIZE]
                  for b in range(0, len(cipher_text), AES_BLOCK_SIZE)]
        message_guess_blocks = []
        for i in range(0, len(blocks) - 1):
            mbg = [chr(0)]*AES_BLOCK_SIZE
            attempt_func = self._attempt_func(blocks, i)
            for byte_num in range(1, AES_BLOCK_SIZE+1):
                pad = chr(0)*(AES_BLOCK_SIZE-byte_num) + chr(byte_num)*byte_num
                for g in self.GUESS_ORDER:
                    mbg[-byte_num] = chr(g)
                    attempt = attempt_func(pad, mbg)
                    if (self.query(attempt.encode("hex"))):
                        break
                print(mbg)
            message_guess_blocks.append(''.join(mbg))
        return (''.join(message_guess_blocks)).encode("hex")






if __name__ == "__main__":
    po = PaddingOracle()
    print(po.cipher_text_guess(CIPHER_TEXT))
