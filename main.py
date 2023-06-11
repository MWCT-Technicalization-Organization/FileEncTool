import os
import mmap
import time
from concurrent.futures import ThreadPoolExecutor
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from tqdm import tqdm
import warnings

# Warning module for raising warnings
class ModeWarning(Warning):
    pass

def warning(message):
    warnings.warn(message, ModeWarning)

# Custom FileError exception
class FileError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

# Remove duplicate file module
def remove_duplicate_file(backpath, show_feedback):
    if not show_feedback:
        os.remove(backpath)
    else:
        none = True
        while none:
            check = str(input('The output file already exists, do you want to delete it (Y/N)\n'))
            if check == 'Y' or check == 'y':
                os.remove(backpath)
                print('Deletion completed')
                none = False
            elif check == 'N' or check == 'n':
                none = False
                raise FileError('Duplicate file')
            else:
                print('Unknown input value')

# Generate RSA key pair module
def generate_rsa_keypair_file(priv_file, pub_file, show_feedback):
    if os.path.exists(priv_file):
        remove_duplicate_file(priv_file, show_feedback)
    if os.path.exists(pub_file):
        remove_duplicate_file(pub_file, show_feedback)
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    with open(priv_file, 'w') as pvk, open(pub_file, 'w') as puk:
        pvk.write(private_key)
        puk.write(public_key)
    if show_feedback:
        print(f'Generation successful. Private key saved to {priv_file}, public key saved to {pub_file}')

# Hybrid encryption module
def rsa_aes_encrypt(file_path, backpath, rsa_cipher, show_feedback):
    with open(file_path, 'rb') as r, open(backpath, 'wb') as wr:
        with mmap.mmap(r.fileno(), length=0, access=mmap.ACCESS_READ) as mmapped_file:
            data = mmapped_file.read()
            aes_key = os.urandom(32)
            enc_aes_key = rsa_cipher.encrypt(aes_key)
            cipher = AES.new(aes_key, AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(data)
            wr.write(enc_aes_key + cipher.nonce + tag + ciphertext)
    if show_feedback:
        print(f'Encryption completed. Encrypted file saved to: {backpath}')

# Hybrid decryption module
def rsa_aes_decrypt(file_path, backpath, rsa_cipher, show_feedback):
    with open(file_path, 'rb') as r, open(backpath, 'wb') as wr:
        with mmap.mmap(r.fileno(), length=0, access=mmap.ACCESS_READ) as mmapped_file:
            enc_aes_key = mmapped_file.read(256)
            ciphertext = mmapped_file.read()
            aes_key = rsa_cipher.decrypt(enc_aes_key)
            nonce = ciphertext[:16]
            tag = ciphertext[16:32]
            enc_data = ciphertext[32:]
            cipher = AES.new(aes_key, AES.MODE_EAX, nonce)
            data = cipher.decrypt_and_verify(enc_data, tag)
            wr.write(data)
    if show_feedback:
        print(f'Decryption completed. Decrypted file saved to: {backpath}')

# Pure RSA encryption module
def rsa_encrypt(file_path, backpath, cipher, use_multithreading, show_progress, show_feedback):
    warning("It is foolish to use pure RSA encryption without considering file size and necessity. "
            "Although pure RSA is secure, it is very inefficient.")
    chunk_size = 200
    results = {}
    if show_feedback:
        print(f'Starting encryption. Please wait.')
    t = time.time()
    file_size = os.path.getsize(file_path)
    pbar = None
    if show_progress:
        pbar = tqdm(total=file_size, unit='B', unit_scale=True)

    def func(i, cipher, data, results):
        encrypted_data = cipher.encrypt(data)
        results[i] = encrypted_data
        if show_progress:
            pbar.update(len(data))

    with open(file_path, 'rb') as read_file, open(backpath, 'ab') as write_file:
        with mmap.mmap(read_file.fileno(), length=0, access=mmap.ACCESS_READ) as read_mmap:
            if use_multithreading:
                executor = ThreadPoolExecutor(max_workers=None)
            else:
                executor = None

            def threaded(i):
                offset = i * chunk_size
                data = read_mmap[offset:offset + chunk_size]
                func(i, cipher, data, results)

            for i in range(file_size // chunk_size + 1):
                if use_multithreading:
                    executor.submit(threaded, i)
                else:
                    threaded(i)

            if use_multithreading:
                executor.shutdown(wait=True)

        for i in range(file_size // chunk_size + 1):
            if i in results:
                data = results[i]
                if data:
                    write_file.write(data)

    if pbar:
        pbar.close()
    spendtime = time.time() - t
    if show_feedback:
        print(f'Encryption completed. Time taken: {spendtime:.2f}s. Encrypted file saved to: {backpath}')

# Pure RSA decryption module
def rsa_decrypt(file_path, backpath, cipher, use_multithreading, show_progress, show_feedback):
    warning("It is foolish to use pure RSA encryption without considering file size and necessity. "
            "Although pure RSA is secure, it is very inefficient.")
    chunk_size = 256
    results = {}
    if show_feedback:
        print(f'Starting decryption. Please wait.')
    t = time.time()
    file_size = os.path.getsize(file_path)
    pbar = None
    if show_progress:
        pbar = tqdm(total=file_size, unit='B', unit_scale=True)

    def func(i, cipher, data, results):
        encrypted_data = cipher.decrypt(data)
        results[i] = encrypted_data
        if show_progress:
            pbar.update(len(data))

    with open(file_path, 'rb') as read_file, open(backpath, 'ab') as write_file:
        with mmap.mmap(read_file.fileno(), length=0, access=mmap.ACCESS_READ) as read_mmap:
            if use_multithreading:
                executor = ThreadPoolExecutor(max_workers=None)
            else:
                executor = None

            def threaded(i):
                offset = i * chunk_size
                data = read_mmap[offset:offset + chunk_size]
                func(i, cipher, data, results)

            for i in range(file_size // chunk_size + 1):
                if use_multithreading:
                    executor.submit(threaded, i)
                else:
                    threaded(i)

            if use_multithreading:
                executor.shutdown(wait=True)

        for i in range(file_size // chunk_size + 1):
            if i in results:
                data = results[i]
                if data:
                    write_file.write(data)

    if pbar:
        pbar.close()
    spendtime = time.time() - t
    if show_feedback:
        print(f'Decryption completed. Time taken: {spendtime:.2f}s. Decrypted file saved to: {backpath}')

# Function dispatcher
def process_file(file_path: str, key_path: str, backpath: str,
                 enc: bool, aes: bool,
                 use_multithreading: bool, show_progress: bool, show_feedback: bool):
    with open(key_path, 'r') as key_file:
        key_data = key_file.read()

    rsa_key = RSA.import_key(key_data)
    cipher = PKCS1_OAEP.new(rsa_key)

    if os.path.exists(backpath):
        remove_duplicate_file(backpath, show_feedback)

    if not os.path.exists(key_path):
        raise FileError('The key file does not exist')

    if aes:
        if enc:
            rsa_aes_encrypt(file_path, backpath, cipher, show_feedback)
        else:
            rsa_aes_decrypt(file_path, backpath, cipher, show_feedback)
    else:
        if enc:
            rsa_encrypt(file_path, backpath, cipher, use_multithreading, show_progress, show_feedback)
        else:
            rsa_decrypt(file_path, backpath, cipher, use_multithreading, show_progress, show_feedback)


# The following are the guide parts

def generate_rsa_keypair(priv_file, pub_file, show_feedback: bool = True):
    """
    Generate an RSA key pair and save the private and public keys to files.

    Args:
        priv_file: Path to the file where the private key will be saved.
        pub_file: Path to the file where the public key will be saved.
        show_feedback: (optional) Whether to display feedback messages. Defaults to True.
    """
    generate_rsa_keypair_file(priv_file, pub_file, show_feedback)


def rsa_aes_encrypt_file(file_path: str, key_path: str, backpath: str,
                         show_feedback: bool = True):
    """
    Encrypt a file using a hybrid RSA-AES encryption scheme.

    Args:
        file_path: Path to the file to be encrypted.
        key_path: Path to the RSA key file.
        backpath: Path to save the encrypted file.
        show_feedback: (optional) Whether to display feedback messages. Defaults to True.
    """
    enc = True
    aes = True
    process_file(file_path, key_path, backpath, enc, aes,
                 False, False, show_feedback)


def rsa_aes_decrypt_file(file_path: str, key_path: str, backpath: str,
                         show_feedback: bool = True):
    """
    Decrypt a file encrypted using a hybrid RSA-AES encryption scheme.

    Args:
        file_path: Path to the encrypted file.
        key_path: Path to the RSA key file.
        backpath: Path to save the decrypted file.
        show_feedback: (optional) Whether to display feedback messages. Defaults to True.
    """
    enc = False
    aes = True
    process_file(file_path, key_path, backpath, enc, aes,
                 False, False, show_feedback)


def rsa_encrypt_file(file_path: str, key_path: str, backpath: str,
                     use_multithreading: bool = True, show_progress: bool = True,
                     show_feedback: bool = True):
    """
    Encrypt a file using pure RSA encryption.

    Args:
        file_path: Path to the file to be encrypted.
        key_path: Path to the RSA key file.
        backpath: Path to save the encrypted file.
        use_multithreading: (optional) Whether to use multithreading for encryption. Defaults to True.
        show_progress: (optional) Whether to display a progress bar. Defaults to True.
        show_feedback: (optional) Whether to display feedback messages. Defaults to True.
    """
    enc = True
    aes = False
    process_file(file_path, key_path, backpath, enc, aes,
                 use_multithreading, show_progress, show_feedback)


def rsa_decrypt_file(file_path: str, key_path: str, backpath: str,
                     use_multithreading: bool = True, show_progress: bool = True,
                     show_feedback: bool = True):
    """
    Decrypt a file encrypted using pure RSA encryption.

    Args:
        file_path: Path to the encrypted file.
        key_path: Path to the RSA key file.
        backpath: Path to save the decrypted file.
        use_multithreading: (optional) Whether to use multithreading for decryption. Defaults to True.
        show_progress: (optional) Whether to display a progress bar. Defaults to True.
        show_feedback: (optional) Whether to display feedback messages. Defaults to True.
    """
    enc = False
    aes = False
    process_file(file_path, key_path, backpath, enc, aes,
                 use_multithreading, show_progress, show_feedback)
