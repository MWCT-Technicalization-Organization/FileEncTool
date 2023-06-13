中文文档请访问[README_zh.md](https://github.com/MWCT-Technicalization-Organization/FileEncTool/edit/main/README_zh.md)
# encfile Official Documentation

## Introduction

Welcome to the encfile library documentation! encfile is a powerful Python library that provides file encryption and decryption functionality. It uses the RSA encryption algorithm and the AES encryption algorithm, supporting both hybrid RSA-AES encryption and pure RSA encryption schemes.

## Installation

You can install the encfile library using the pip command:

```shell
pip install FileEncTool
```

## Usage Examples

### Generating RSA Key Pair

To generate an RSA key pair and save the private key and public key to files, you can use the `generate_rsa_keypair` function:

```python
from encfile import generate_rsa_keypair

# Generate an RSA key pair and save to files
generate_rsa_keypair(priv_file='private_key.pem', pub_file='public_key.pem')
```

You can specify the paths for the private key file and public key file. By default, feedback messages are displayed during the key generation process. You can disable the feedback messages by setting the `show_feedback` parameter to `False`, as shown below:

```python
from encfile import generate_rsa_keypair

# Generate an RSA key pair and save to files
generate_rsa_keypair(priv_file='private_key.pem', pub_file='public_key.pem', show_feedback=False)
```

### Hybrid RSA-AES Encryption

To encrypt a file using the hybrid RSA-AES encryption scheme, you can use the `rsa_aes_encrypt_file` function:

```python
from encfile import rsa_aes_encrypt_file

# Encrypt a file using hybrid RSA-AES encryption
rsa_aes_encrypt_file(file_path='plaintext.txt', key_path='public_key.pem', backpath='encrypted_file.enc')
```

You need to provide the path of the file to be encrypted, the path of the RSA public key file, and the path to save the encrypted file. By default, feedback messages are displayed during the encryption process. You can disable the feedback messages by setting the `show_feedback` parameter to `False`, similar to the previous examples.

### Hybrid RSA-AES Decryption

To decrypt a file encrypted using the hybrid RSA-AES encryption scheme, you can use the `rsa_aes_decrypt_file` function:

```python
from encfile import rsa_aes_decrypt_file

# Decrypt a file encrypted using hybrid RSA-AES encryption
rsa_aes_decrypt_file(file_path='encrypted_file.enc', key_path='private_key.pem', backpath='decrypted_file.txt')
```

You need to provide the path of the encrypted file, the path of the RSA private key file, and the path to save the decrypted file. By default, feedback messages are displayed during the decryption process. You can disable the feedback messages by setting the `show_feedback` parameter to `False`, as mentioned above.

### Pure RSA Encryption

To encrypt a file using the pure RSA encryption scheme, you can use the `rsa_encrypt_file` function:

```python
from encfile import rsa_encrypt_file

# Encrypt a file using pure RSA encryption
rsa_encrypt_file(file_path='plaintext.txt', key_path='public_key.pem', backpath='encrypted_file.enc', use_multithreading=False, show_progress=False, show_feedback=False)
```

You need to provide the path of the file to be encrypted, the path of the RSA public key file, and the path to save the encrypted file. By default, the encryption process uses multithreading and displays a progress bar. You can disable multithreading by setting the `use_multithreading` parameter to `False` and disable the progress bar by setting the `show_progress` parameter to `False`. By default, feedback messages are displayed during the encryption process. You can disable the feedback messages by setting the `show_feedback` parameter to `False`, as shown in the code above.

###

 Pure RSA Decryption

To decrypt a file encrypted using the pure RSA encryption scheme, you can use the `rsa_decrypt_file` function:

```python
from encfile import rsa_decrypt_file

# Decrypt a file encrypted using pure RSA encryption
rsa_decrypt_file(file_path='encrypted_file.enc', key_path='private_key.pem', backpath='decrypted_file.txt')
```

You need to provide the path of the encrypted file, the path of the RSA private key file, and the path to save the decrypted file. By default, feedback messages are displayed during the decryption process. You can disable the feedback messages by setting the `show_feedback` parameter to `False`, as mentioned above.

## Conclusion

The encfile library provides convenient asymmetric file encryption and decryption capabilities. You can use either the RSA-AES hybrid encryption or the pure RSA encryption scheme to protect your files. Make sure to securely store your private key file to prevent data leaks. If you have any further questions, please refer to the comments in the __init__.py file or contact the author.

## License

This project is licensed under the AGPL 3.0 license. See the [LICENSE](https://github.com/MWCT-Technicalization-Organization/File_Encryption_Tool/blob/main/LICENSE) file for details.
