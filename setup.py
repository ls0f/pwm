# coding:utf-8

from setuptools import setup, find_packages

PACKAGE = "pwm-tool3"
NAME = "pwm-tool3"
DESCRIPTION = "password manager tool"
AUTHOR = "lovedboy"
AUTHOR_EMAIL = "lovedboy.tk@qq.com"
URL = "https://github.com/ls0f/pwm"
VERSION = '0.3.2'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    package_data={'': ['*.txt', '*.TXT']},
    include_package_data=True,
    scripts=['bin/pwm'],
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    zip_safe=False,
)
