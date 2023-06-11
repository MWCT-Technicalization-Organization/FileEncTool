# 文件加密工具

文件加密工具是一个使用RSA和AES算法提供文件加密和解密功能的Python库和命令行工具。

## 特性

- 生成RSA密钥对
- 使用RSA和AES加密文件
- 使用纯RSA加密文件
- 支持多线程和进度跟踪

## 安装

使用pip安装文件加密工具：

```shell
pip install FileEncTool
```

## 使用方法

### 生成RSA密钥对

```python
from encfile import generate_rsa_keypair

priv_file = "private.pem"
pub_file = "public.pem"

generate_rsa_keypair(priv_file, pub_file)
```

### 使用RSA和AES加密文件

```python
from encfile import rsa_aes_encrypt_file

file_path = "plaintext.txt"
key_path = "public.pem"
backpath = "encrypted_file.txt"

rsa_aes_encrypt_file(file_path, key_path, backpath)
```

### 使用RSA和AES解密文件

```python
from encfile import rsa_aes_decrypt_file

file_path = "encrypted_file.txt"
key_path = "private.pem"
backpath = "decrypted_file.txt"

rsa_aes_decrypt_file(file_path, key_path, backpath)
```

### 使用纯RSA加密文件

```python
from encfile import rsa_encrypt_file

file_path = "plaintext.txt"
key_path = "public.pem"
backpath = "encrypted_file.txt"

rsa_encrypt_file(file_path, key_path, backpath)
```

### 使用纯RSA解密文件

```python
from encfile import rsa_decrypt_file

file_path = "encrypted_file.txt"
key_path = "private.pem"
backpath = "decrypted_file.txt"

rsa_decrypt_file(file_path, key_path, backpath)
```

## 文档

有关更多详细信息和高级用法，请参阅[文档](https://github.com/MWCT-Technicalization-Organization/File_Encryption_Tool)。

## 许可证

本项目基于AGPL 3.0许可证进行许可。详细信息请参阅[LICENSE](https://github.com/MWCT-Technicalization-Organization/File_Encryption_Tool)文件。
