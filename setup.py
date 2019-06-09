# coding:utf-8

from setuptools import setup, find_packages

PACKAGE = "pwm-tool"
NAME = "pwm-tool"
DESCRIPTION = "password manager tool"
AUTHOR = "lovedboy"
AUTHOR_EMAIL = "lovedboy.tk@qq.com"
URL = "https://github.com/ls0f/pwm"
VERSION = '0.3.1'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
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
