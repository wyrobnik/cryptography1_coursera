import argparse


def encrypt_cbc_aes(key, pt):
    pass

def decrypt_cbc_aes(key, ct):
    pass

def encrypt_ctr_aes(key, pt):
    pass

def decrypt_ctr_aes(key, ct):
    pass

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

    if (args.mode == "cbc"):
        if (arg.encrypt):
            encrypt_cbc_aes(arg.key, arg.text)
        else:
            decrypt_cbc_aes(arg.key, arg.text)
    elif (args.mode == "ctr"):
        if (arg.encrypt):
            encrypt_ctr_aes(arg.key, arg.text)
        else:
            decrypt_ctr_aes(arg.key, arg.text)
    else:
        print("mode needs to either be 'cbc' or 'ctr'.")
        exit(1)
