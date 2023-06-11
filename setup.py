from setuptools import setup

setup(
    name='FileEncTool',
    version='1.5',
    packages=['encfile'],
    url='https://github.com/MWCT-Technicalization-Organization/File_Encryption_Tool',
    license='AGPL3.0',
    author='核善的小兲',
    author_email='to@mwtour.cn',
    description='File Encryption Tool——A powerful asymmetric file encryption Python library.',
    install_requires=['pycryptodome','tqdm'],
    long_description=open(r'C:\Users\Abner\Documents\encfile\README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
)