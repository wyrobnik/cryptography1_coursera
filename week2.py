import argparse
from Crypto.Cipher import AES
from Crypto import Random

AES_BLOCK_SIZE = 16

def encrypt_cbc_aes(key, pt):
    cipher = AES.new(key, AES.MODE_ECB)
    iv = make_iv()

    # pad the pt
    padding = AES_BLOCK_SIZE - (len(pt) % AES_BLOCK_SIZE)
    pt += chr(padding)*padding

    ct = [iv]
    previous_encrypted_block = iv
    for i in range(0, len(pt), AES_BLOCK_SIZE):
        block = pt[i:i+AES_BLOCK_SIZE]

        xored = xor(previous_encrypted_block, block)
        encrypted_block = cipher.encrypt(xored)
        ct.append(encrypted_block)

        previous_encrypted_block = encrypted_block

    return ''.join(ct)

def decrypt_cbc_aes(key, ct):
    cipher = AES.new(key, AES.MODE_ECB)
    pt = []
    for i in range(AES_BLOCK_SIZE, len(ct), AES_BLOCK_SIZE):
        decrypted_block = cipher.decrypt(ct[i:i+AES_BLOCK_SIZE])
        message_block = xor(ct[i-AES_BLOCK_SIZE:i], decrypted_block)
        pt.append(message_block)

    pt = ''.join(pt)

    # Remove padding
    padding = ord(pt[-1])
    pt = pt[:-padding]

    return pt

def encrypt_ctr_aes(key, pt):
    iv = make_iv()
    return iv + ctr_aes(key, iv, pt)

def decrypt_ctr_aes(key, ct):
    return ctr_aes(key, ct[:AES_BLOCK_SIZE], ct[AES_BLOCK_SIZE:])

def ctr_aes(key, iv, text):
    cipher = AES.new(key, AES.MODE_ECB)
    output = []
    for i in range(0, len(text), AES_BLOCK_SIZE):
        block = text[i:i+AES_BLOCK_SIZE]
        prf_result = cipher.encrypt(iv)
        output.append(xor(prf_result, block))
        iv = increment_string(iv)
    return ''.join(output)

def make_iv():
    return Random.get_random_bytes(AES_BLOCK_SIZE)

def xor(block1, block2):
    return ''.join([chr(ord(x) ^ ord(y)) for x, y in zip(block1, block2)])

def increment_string(input):
    bytelist = [ord(c) for c in input]
    carry = 1
    for i in range(len(bytelist) - 1, -1, -1):
        new_byte = bytelist[i] + carry
        carry = new_byte >= 256
        bytelist[i] = new_byte % 256
    return ''.join([chr(b) for b in bytelist])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument("mode", help="cbc or ctr", type=str)
    parser.add_argument("key", help="key to use (in hex)", type=str)
    parser.add_argument("text", help="ciper text (hex) or plain text",
                        type=str)
    parser.add_argument("-e", "--encrypt",
                        help="encrypt flag (otherwise will decrypt)",
                        action="store_true")
    args = parser.parse_args()

    key = args.key.decode('hex')
    if (args.mode == "cbc"):
        if (args.encrypt):
            print(encrypt_cbc_aes(key, args.text).encode('hex'))
        else:
            print(decrypt_cbc_aes(key, args.text.decode('hex')))
    elif (args.mode == "ctr"):
        if (args.encrypt):
            print(encrypt_ctr_aes(key, args.text).encode('hex'))
        else:
            print(decrypt_ctr_aes(key, args.text.decode('hex')))
    else:
        print("mode needs to either be 'cbc' or 'ctr'.")
        exit(1)
