from Crypto.Hash import SHA256

FILE = "ignored_files/6.1.intro.mp4_download"
OUTPUT_FILE = FILE + '_mac'
KB_SIZE = 1024
HASH_BYTES = 32

def compute_hash(block):
    hash = SHA256.new()
    hash.update(block)
    return hash.digest()

def compute_file_hash_and_store(file_path, output_path):
    kb_blocks = []
    with open(file_path, 'r') as f:
        content = f.read()
        kb_blocks = [content[i:i+KB_SIZE] for i in xrange(0, len(content), KB_SIZE)]
    
    h = ""
    content_mac = []
    for block in kb_blocks[::-1]:
        content_mac.append(block + h)
        h = compute_hash(block + h)
    
    with open(output_path, 'w') as f:
        for block in content_mac[::-1]:
            f.write(block)
    
    return h

def verify_file_hash(file_path, hash0):
    with open(file_path, 'r') as f:
        content = f.read()
        blocks = [content[i:i+KB_SIZE+HASH_BYTES] for i in xrange(0, len(content), KB_SIZE+HASH_BYTES)]
        transmitted_hash = hash0
        for block in blocks:
            computed_hash = compute_hash(block)
            if (computed_hash != transmitted_hash):
                print("Unverified block received, stopping")
                return False
            transmitted_hash = block[-HASH_BYTES:]
    print("File verified!")
    return True

if __name__ == "__main__":
    hash0 = compute_file_hash_and_store(FILE, OUTPUT_FILE)
    print(hash0.encode('hex'))
    print(verify_file_hash(OUTPUT_FILE, hash0))