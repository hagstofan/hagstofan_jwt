"""
Install script for a package providing auth with JWTs
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="auth_utils",
    version='0.0.1',
    description='JWT authorization module for hagstofan',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'requests==2.24.0',
        'python-jose==3.1.0',
        'PyJWT==1.7.1',
        'cryptography==2.9.2'
    ]
)
