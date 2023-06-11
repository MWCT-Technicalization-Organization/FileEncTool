from setuptools import setup

setup(
    name='file-encryption-tool',
    version='1.0',
    packages=['.'],
    url='https://github.com/MWCT-Technicalization-Organization/File_Encryption_Tool',
    license='AGPL3.0',
    author='核善的小兲',
    author_email='to@mwtour.cn',
    description='File Encryption Tool——A powerful asymmetric file encryption Python library.',
    requires=['pycryptodome','tqdm'],
)