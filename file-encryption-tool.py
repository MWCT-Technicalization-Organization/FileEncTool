import os
import mmap
import time
from concurrent.futures import ThreadPoolExecutor
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from tqdm import tqdm


class FileError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def remove_duplicate_file(backpath, show_feedback):
    if not show_feedback:
        os.remove(backpath)
    else:
        none = True
        while none:
            check = str(input('输出文件已存在，是否删除（Y/N）\n'))
            if check == 'Y' or check == 'y':
                os.remove(backpath)
                print('完成删除')
                none = False
            elif check == 'N' or check == 'n':
                none = False
                raise FileError('重复的文件')
            else:
                print('未知的输入值')


def generate_rsa_keypair_file(priv_file, pub_file, show_feedback):
    # 生成RSA密钥对
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
        print(f'生成成功，私钥被保存到了{priv_file}，公钥被保存到了{pub_file}')


def rsa_aes_encrypt(file_path, backpath, rsa_cipher, show_feedback: bool):
    with open(file_path, 'rb') as r, open(backpath, 'wb') as wr:
        with mmap.mmap(r.fileno(), length=0, access=mmap.ACCESS_READ) as mmapped_file:
            data = mmapped_file.read()
            aes_key = os.urandom(32)
            enc_aes_key = rsa_cipher.encrypt(aes_key)
            cipher = AES.new(aes_key, AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(data)
            wr.write(enc_aes_key + cipher.nonce + tag + ciphertext)
    if show_feedback:
        print(f'加密完成，加密文件保存在：{backpath}')


def rsa_aes_decrypt(file_path, backpath, rsa_cipher, show_feedback: bool):
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
        print(f'解密完成，解密文件保存在：{backpath}')


def rsa_encrypt(file_path, backpath, cipher, use_multithreading, show_progress, show_feedback):
    chunk_size = 200
    results = {}
    if show_feedback:
        print(f'开始加密，请耐心等待')
    t = time.time()
    pbar = None
    if show_progress:
        pbar = tqdm(total=os.path.getsize(file_path) // chunk_size + 1, unit='线程')

    def func(i, cipher, data, results):
        encrypted_data = cipher.encrypt(data)
        results[i] = encrypted_data
        if show_progress:
            pbar.update(1)

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

            for i in range(os.path.getsize(file_path) // chunk_size + 1):
                if use_multithreading:
                    executor.submit(threaded, i)
                else:
                    threaded(i)

            if use_multithreading:
                executor.shutdown(wait=True)

        for i in range(os.path.getsize(file_path) // chunk_size + 1):
            if i in results:
                data = results[i]
                if data:
                    write_file.write(data)

    if pbar:
        pbar.close()
    spendtime = time.time() - t
    if show_feedback:
        print(f'加密完成，花费{spendtime:.2f}s，加密文件保存在：{backpath}')


import os
import mmap
import time
from concurrent.futures import ThreadPoolExecutor
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from tqdm import tqdm


class FileError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def remove_duplicate_file(backpath, show_feedback):
    """
    删除重复的文件
    Remove duplicate files

    Args:
        backpath (str): 输出文件路径 / Output file path
        show_feedback (bool): 是否显示反馈信息 / Whether to show feedback
    """
    if not show_feedback:
        os.remove(backpath)
    else:
        none = True
        while none:
            check = str(input('输出文件已存在，是否删除（Y/N）\nThe output file already exists. Do you want to delete it? (Y/N)\n'))
            if check == 'Y' or check == 'y':
                os.remove(backpath)
                print('完成删除\nDeletion completed.')
                none = False
            elif check == 'N' or check == 'n':
                none = False
                raise FileError('重复的文件\nDuplicate file.')
            else:
                print('未知的输入值\nUnknown input value.')


def generate_rsa_keypair_file(priv_file, pub_file, show_feedback):
    """
    生成RSA密钥对
    Generate RSA key pair

    Args:
        priv_file (str): 私钥文件路径 / Private key file path
        pub_file (str): 公钥文件路径 / Public key file path
        show_feedback (bool): 是否显示反馈信息 / Whether to show feedback
    """
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
        print(f'生成成功，私钥被保存到了{priv_file}，公钥被保存到了{pub_file}\nKey generation successful. Private key saved to {priv_file}. Public key saved to {pub_file}')


def rsa_aes_encrypt(file_path, backpath, rsa_cipher, show_feedback: bool):
    """
    RSA和AES加密
    RSA and AES encryption

    Args:
        file_path (str): 待加密的文件路径 / Path of the file to be encrypted
        backpath (str): 加密后的文件保存路径 / Encrypted file save path
        rsa_cipher (PKCS1_OAEP): RSA加密器 / RSA encryptor
        show_feedback (bool): 是否显示反馈信息 / Whether to show feedback
    """
    with open(file_path, 'rb') as r, open(backpath, 'wb') as wr:
        with mmap.mmap(r.fileno(), length=0, access=mmap.ACCESS_READ) as mmapped_file:
            data = mmapped_file.read()
            aes_key = os.urandom(32)
            enc_aes_key = rsa_cipher.encrypt(aes_key)
            cipher = AES.new(aes_key, AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(data)
            wr.write(enc_aes_key + cipher.nonce + tag + ciphertext)
    if show_feedback:
        print(f'加密完成，加密文件保存在：{backpath}\nEncryption completed. Encrypted file saved to: {backpath}')


def rsa_aes_decrypt(file_path, key_path, backpath, use_multithreading=False, show_progress=False, show_feedback=True):
    """
    使用纯RSA解密文件
    Decrypt a file using pure RSA encryption

    Args:
        file_path (str): 待解密的文件路径 / Path of the file to be decrypted
        key_path (str): RSA私钥文件路径 / RSA private key file path
        backpath (str): 解密后的文件保存路径 / Decrypted file save path
        use_multithreading (bool): 是否使用多线程处理 / Whether to use multithreading processing
        show_progress (bool): 是否显示进度条 / Whether to show progress bar
        show_feedback (bool): 是否显示反馈信息 / Whether to show feedback
    """
    with open(key_path, 'r') as key_file:
        private_key = RSA.import_key(key_file.read())

    if use_multithreading:
        if show_feedback:
            print("使用多线程解密...\nDecrypting with multiple threads...")
        executor = ThreadPoolExecutor(max_workers=os.cpu_count())
        futures = []
        with open(file_path, 'rb') as r, open(backpath, 'wb') as wr:
            with mmap.mmap(r.fileno(), length=0, access=mmap.ACCESS_READ) as mmapped_file:
                if show_progress:
                    file_size = os.path.getsize(file_path)
                    pbar = tqdm(total=file_size, unit='B', unit_scale=True)
                while True:
                    enc_aes_key = mmapped_file.read(256)
                    if not enc_aes_key:
                        break
                    ciphertext = mmapped_file.read(256)
                    if not ciphertext:
                        break
                    if show_progress:
                        pbar.update(len(enc_aes_key) + len(ciphertext))
                    futures.append(executor.submit(decrypt_chunk, enc_aes_key, ciphertext, private_key, wr))
        if show_progress:
            pbar.close()
        for future in futures:
            future.result()
    else:
        with open(file_path, 'rb') as r, open(backpath, 'wb') as wr:
            with mmap.mmap(r.fileno(), length=0, access=mmap.ACCESS_READ) as mmapped_file:
                while True:
                    enc_aes_key = mmapped_file.read(256)
                    if not enc_aes_key:
                        break
                    ciphertext = mmapped_file.read(256)
                    if not ciphertext:
                        break
                    decrypt_chunk(enc_aes_key, ciphertext, private_key, wr)

    if show_feedback:
        print(f'解密完成，解密文件保存在：{backpath}\nDecryption completed. Decrypted file saved to: {backpath}')


def decrypt_chunk(enc_aes_key, ciphertext, private_key, output_file):
    """
    解密数据块

    Args:
        enc_aes_key (bytes): 加密的AES密钥 / Encrypted AES key
        ciphertext (bytes): 待解密的密文 / Ciphertext to be decrypted
        private_key (RSA._RSAobj): RSA私钥对象 / RSA private key object
        output_file (file): 输出文件对象 / Output file object
    """
    aes_key = private_key.decrypt(enc_aes_key)
    nonce = ciphertext[:16]
    tag = ciphertext[16:32]
    enc_data = ciphertext[32:]

    cipher = AES.new(aes_key, AES.MODE_EAX, nonce)
    data = cipher.decrypt(enc_data)
    output_file.write(data)


def rsa_decrypt(file_path, backpath, cipher, use_multithreading, show_progress, show_feedback):
    """
    使用纯RSA解密文件

    Args:
        file_path (str): 待解密的文件路径 / Path of the file to be decrypted
        backpath (str): 解密后的文件保存路径 / Decrypted file save path
        cipher (PKCS1_OAEP): RSA加密器对象 / RSA cipher object
        use_multithreading (bool): 是否使用多线程处理 / Whether to use multithreading processing
        show_progress (bool): 是否显示进度条 / Whether to show progress bar
        show_feedback (bool): 是否显示反馈信息 / Whether to show feedback
    """
    chunk_size = 256
    results = {}
    if show_feedback:
        print('开始解密，请耐心等待\nDecryption started. Please wait patiently.')
    t = time.time()
    pbar = None
    if show_progress:
        pbar = tqdm(total=os.path.getsize(file_path) // chunk_size + 1, unit='线程/Thread')

    def func(i, cipher, data, results):
        encrypted_data = cipher.decrypt(data)
        results[i] = encrypted_data
        if show_progress:
            pbar.update(1)

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

            for i in range(os.path.getsize(file_path) // chunk_size + 1):
                if use_multithreading:
                    executor.submit(threaded, i)
                else:
                    threaded(i)

            if use_multithreading:
                executor.shutdown(wait=True)

        for i in range(os.path.getsize(file_path) // chunk_size + 1):
            if i in results:
                data = results[i]
                if data:
                    write_file.write(data)

    if pbar:
        pbar.close()
    spendtime = time.time() - t
    if show_feedback:
        print(f'解密完成，花费{spendtime:.2f}s，解密文件保存在：{backpath}\nDecryption completed. Time taken: {spendtime:.2f}s. Decrypted file saved to: {backpath}')


def process_file(file_path: str, key_path: str, backpath: str,
                 enc: bool, aes: bool,
                 use_multithreading: bool, show_progress: bool, show_feedback: bool):
    """
    处理文件
    Process a file

    Args:
        file_path (str): 待处理的文件路径 / Path of the file to be processed
        key_path (str): 密钥文件路径 / Key file path
        backpath (str): 处理后的文件保存路径 / Processed file save path
        enc (bool): 是否加密 / Whether to encrypt
        aes (bool): 是否使用AES加密 / Whether to use AES encryption
        use_multithreading (bool): 是否使用多线程处理 / Whether to use multithreading processing
        show_progress (bool): 是否显示进度条 / Whether to show progress bar
        show_feedback (bool): 是否显示反馈信息 / Whether to show feedback
    """
    with open(key_path, 'r') as key_file:
        key_data = key_file.read()

    rsa_key = RSA.import_key(key_data)
    cipher = PKCS1_OAEP.new(rsa_key)

    if os.path.exists(backpath):
        remove_duplicate_file(backpath, show_feedback)

    if not os.path.exists(key_path):
        raise FileError('不存在的密钥文件\nNon-existent key file')

    if aes:
        if enc:
            rsa_aes_encrypt(file_path, backpath, cipher, show_feedback)
        else:
            rsa_aes_decrypt(file_path, key_path, backpath, show_feedback)
    else:
        if enc:
            rsa_encrypt(file_path, backpath, cipher, use_multithreading, show_progress, show_feedback)
        else:
            rsa_decrypt(file_path, backpath, cipher, use_multithreading, show_progress, show_feedback)


def generate_rsa_keypair(priv_file, pub_file, show_feedback=True):
    """
    生成RSA密钥对
    Generate RSA key pair

    Args:
        priv_file (str): 私钥文件路径 / Private key file path
        pub_file (str): 公钥文件路径 / Public key file path
        show_feedback (bool): 是否显示反馈信息 / Whether to show feedback
    """
    generate_rsa_keypair_file(priv_file, pub_file, show_feedback)


def rsa_aes_encrypt_file(file_path: str, key_path: str, backpath: str,
                         show_feedback: bool = True):
    """
    RSA和AES加密文件
    Encrypt a file using RSA and AES encryption

    Args:
        file_path (str): 待加密的文件路径 / Path of the file to be encrypted
        key_path (str): RSA公钥文件路径 / RSA public key file path
        backpath (str): 加密后的文件保存路径 / Encrypted file save path
        show_feedback (bool): 是否显示反馈信息 / Whether to show feedback
    """
    enc = True
    aes = True
    process_file(file_path, key_path, backpath, enc, aes,
                 show_feedback=show_feedback)


def rsa_aes_decrypt_file(file_path: str, key_path: str, backpath: str,
                         show_feedback: bool = True):
    """
    RSA和AES解密文件
    Decrypt a file using RSA and AES encryption

    Args:
        file_path (str): 待解密的文件路径 / Path of the file to be decrypted
        key_path (str): RSA私钥文件路径 / RSA private key file path
        backpath (str): 解密后的文件保存路径 / Decrypted file save path
        show_feedback (bool): 是否显示反馈信息 / Whether to show feedback
    """
    enc = False
    aes = True
    process_file(file_path, key_path, backpath, enc, aes,
                 show_feedback=show_feedback)


def rsa_encrypt_file(file_path: str, key_path: str, backpath: str,
                     use_multithreading: bool = True, show_progress: bool = True,
                     show_feedback: bool = True):
    """
    使用纯RSA加密文件
    Encrypt a file using pure RSA encryption

    Args:
        file_path (str): 待加密的文件路径 / Path of the file to be encrypted
        key_path (str): RSA公钥文件路径 / RSA public key file path
        backpath (str): 加密后的文件保存路径 / Encrypted file save path
        use_multithreading (bool): 是否使用多线程处理 / Whether to use multithreading processing
        show_progress (bool): 是否显示进度条 / Whether to show progress bar
        show_feedback (bool): 是否显示反馈信息 / Whether to show feedback
    """
    enc = True
    aes = False
    process_file(file_path, key_path, backpath, enc, aes,
                 use_multithreading, show_progress, show_feedback)


def rsa_decrypt_file(file_path: str, key_path: str, backpath: str,
                     use_multithreading: bool = True, show_progress: bool = True,
                     show_feedback: bool = True):
    """
    使用纯RSA解密文件
    Decrypt a file using pure RSA encryption

    Args:
        file_path (str): 待解密的文件路径 / Path of the file to be decrypted
        key_path (str): RSA私钥文件路径 / RSA private key file path
        backpath (str): 解密后的文件保存路径 / Decrypted file save path
        use_multithreading (bool): 是否使用多线程处理 / Whether to use multithreading processing
        show_progress (bool): 是否显示进度条 / Whether to show progress bar
        show_feedback (bool): 是否显示反馈信息 / Whether to show feedback
    """
    enc = False
    aes = False
    process_file(file_path, key_path, backpath, enc, aes,
                 use_multithreading, show_progress, show_feedback)
