import argparse
from Crypto.Cipher import AES
from Crypto import Random

# TODO clean up
#use MODE.ECB to do single block

def encrypt_cbc_aes(key, pt):
    cipher = AES.new(key, AES.MODE_ECB)
    # 16 byte random IV
    iv = Random.get_random_bytes(16)
    # encrypt pt
    previous_encrypted_block = iv
    ct = []
    for i in range(0, len(pt), 16):
        if (i+16 > len(pt)):
            missing_bytes = i+16-len(pt)
            block = pt[i:len(pt)] + chr(missing_bytes)*missing_bytes
        else:
            block = pt[i:i+16]
        xored = ''.join([chr(ord(x) ^ ord(y)) for x, y in zip(previous_encrypted_block, block)]) # TODO move to separate function
        encrypted_block = cipher.encrypt(xored)
        previous_encrypted_block = encrypted_block
        ct.append(encrypted_block)
    # prepend IV
    ct.insert(0, iv)

    return ''.join(ct).encode('hex')

def decrypt_cbc_aes(key, ct):
    pass

def encrypt_ctr_aes(key, pt):
    pass

def decrypt_ctr_aes(key, ct):
    pass

def bytearray_to_hex_string(b):
    return ''.join('{:02x}'.format(x) for x in b)

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

    key = bytearray_to_hex_string(bytearray.fromhex(args.key)) # TODO better way of turning hex string to string? Look at previous homework
    if (args.mode == "cbc"):
        if (args.encrypt):
            print(encrypt_cbc_aes(key, args.text))
        else:
            print(decrypt_cbc_aes(key, bytearray.fromhex(args.text)))
    elif (args.mode == "ctr"):
        if (args.encrypt):
            print(encrypt_ctr_aes(key, args.text))
        else:
            print(decrypt_ctr_aes(key, bytearray.fromhex(args.text)))
    else:
        print("mode needs to either be 'cbc' or 'ctr'.")
        exit(1)
