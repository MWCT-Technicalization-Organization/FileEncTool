# encfile官方文档

## 简介

欢迎使用encfile库！encfile是一个功能强大的Python库，提供了文件加密和解密功能。它使用RSA加密算法和AES加密算法，支持混合RSA-AES加密和纯RSA加密方案。

## 安装

您可以使用pip命令来安装encfile库：

```shell
pip install FileEncTool
```

## 使用示例

### 生成RSA密钥对

要生成RSA密钥对并将私钥和公钥保存到文件中，您可以使用`generate_rsa_keypair`函数：
```python
from encfile import generate_rsa_keypair

# 生成RSA密钥对并保存到文件
generate_rsa_keypair(priv_file='private_key.pem', pub_file='public_key.pem')
```

您可以指定私钥文件和公钥文件的路径。默认情况下，在生成密钥对的过程中会显示反馈消息。您可以通过将`show_feedback`参数设置为`False`来禁用反馈消息，操作如下：

```python
from encfile import generate_rsa_keypair

# 生成RSA密钥对并保存到文件
generate_rsa_keypair(priv_file='private_key.pem', pub_file='public_key.pem', show_feedback=False)
```

### 混合RSA-AES加密

要使用混合RSA-AES加密方案加密文件，可以使用`rsa_aes_encrypt_file`函数：

```python
from encfile import rsa_aes_encrypt_file

# 使用混合RSA-AES加密加密文件
rsa_aes_encrypt_file(file_path='plaintext.txt', key_path='public_key.pem', backpath='encrypted_file.enc')
```

您需要提供要加密的文件的路径，RSA公钥文件的路径以及保存加密文件的路径。默认情况下，在加密过程中会显示反馈消息。您可以通过将`show_feedback`参数设置为`False`来禁用反馈消息，方法同上。

### 混合RSA-AES解密

要解密使用混合RSA-AES加密方案加密的文件，可以使用`rsa_aes_decrypt_file`函数：

```python
from encfile import rsa_aes_decrypt_file

# 解密使用混合RSA-AES加密的文件
rsa_aes_decrypt_file(file_path='encrypted_file.enc', key_path='private_key.pem', backpath='decrypted_file.txt')
```

您需要提供加密文件的路径，RSA私钥文件的路径以及保存解密文件的路径。默认情况下，在解密过程中会显示反馈消息。您可以通过将`show_feedback`参数设置为`False`来禁用反馈消息，方法同上。

### 纯RSA加密

要使用纯RSA加密方案加密文件，可以使用`rsa_encrypt_file`函数
您需要提供要加密的文件的路径，RSA公钥文件的路径以及保存加密文件的路径。默认情况下，加密过程使用多线程并显示进度条。您可以通过将`use_multithreading`参数设置为`False`来禁用多线程，通过将`show_progress`参数设置为`False`来禁用进度条。默认情况下，在加密过程中会显示反馈消息。您可以通过将`show_feedback`参数设置为`False`来禁用反馈消息。操作如下：
```python
from encfile import rsa_encrypt_file

# 使用纯RSA加密加密文件
rsa_encrypt_file(file_path='plaintext.txt', key_path='public_key.pem', backpath='encrypted_file.enc', use_multithreading=False, show_progress=False, show_feedback=False)
```

### 纯RSA解密

要解密使用纯RSA加密方案加密的文件，可以使用`rsa_decrypt_file`函数：

```python
from encfile import rsa_decrypt_file

# 解密使用纯RSA加密的文件
rsa_decrypt_file(file_path='encrypted_file.enc', key_path='private_key.pem', backpath='decrypted_file.txt')
```

您需要提供加密文件的路径，RSA私钥文件的路径以及保存解密文件的路径。默认情况下，在解密过程中会显示反馈消息。您可以通过将`show_feedback`参数设置为`False`来禁用反馈消息，操作同上

## 结论

encfile库提供了方便的非对称文件加密和解密功能，您可以使用RSA-AES混合加密或纯RSA加密方案来保护您的文件。请确保妥善保管您的私钥文件，以防止数据泄露。如有其他疑问，请查看__init__.py代码注释或联系作者。

## License

本项目使用AGPL 3.0许可证。有关详细信息，请参阅[LICENSE](https://github.com/MWCT-Technicalization-Organization/FileEncTool/blob/main/LICENSE)文件。
