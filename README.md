# File Encryption Tool

The File Encryption Tool is a Python library and command-line tool that provides file encryption and decryption capabilities using RSA and AES algorithms.

## Features

- Generate RSA key pairs
- Encrypt and decrypt files using RSA and AES encryption
- Encrypt and decrypt files using pure RSA encryption
- Support for multithreading and progress tracking

## Installation

Install the File Encryption Tool using pip:

```shell
pip install file-encryption-tool
```

## Usage

### Generate RSA Key Pair

```python
from file_encryption_tool import generate_rsa_keypair

priv_file = "private.pem"
pub_file = "public.pem"

generate_rsa_keypair(priv_file, pub_file)
```

### Encrypt a File using RSA and AES Encryption

```python
from file_encryption_tool import rsa_aes_encrypt_file

file_path = "plaintext.txt"
key_path = "public.pem"
backpath = "encrypted_file.txt"

rsa_aes_encrypt_file(file_path, key_path, backpath)
```

### Decrypt a File using RSA and AES Encryption

```python
from file_encryption_tool import rsa_aes_decrypt_file

file_path = "encrypted_file.txt"
key_path = "private.pem"
backpath = "decrypted_file.txt"

rsa_aes_decrypt_file(file_path, key_path, backpath)
```

### Encrypt a File using Pure RSA Encryption

```python
from file_encryption_tool import rsa_encrypt_file

file_path = "plaintext.txt"
key_path = "public.pem"
backpath = "encrypted_file.txt"

rsa_encrypt_file(file_path, key_path, backpath)
```

### Decrypt a File using Pure RSA Encryption

```python
from file_encryption_tool import rsa_decrypt_file

file_path = "encrypted_file.txt"
key_path = "private.pem"
backpath = "decrypted_file.txt"

rsa_decrypt_file(file_path, key_path, backpath)
```

## Documentation

For more details and advanced usage, please refer to the [documentation](https://github.com/MWCT-Technicalization-Organization/File_Encryption_Tool).

## License

This project is licensed under the GPL-3.0 license. See the [LICENSE](https://github.com/MWCT-Technicalization-Organization/File_Encryption_Tool/blob/main/LICENSE) file for details.
```
