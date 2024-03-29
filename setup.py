# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @File: setup.py
# @Author: SWHL
# @Contact: liekkaskono@163.com
from setuptools import setup

setup(
    name="img_aug_offline",
    version='latest',
    author="SWHL",
    author_email="liekkaskono@163.com",
    description="image augment offline",
    license='Apache-2.0',
    url="https://github.com/SWHL/image_augmentor",
    install_requires=['numpy', 'opencv-python'],
    packages=["img_aug_offline", "img_aug_offline.ops"],  # 用来包含子目录
    entry_points={
        'console_scripts':['img_aug_offline=img_aug_offline.img_aug_offline:main']
    }
)