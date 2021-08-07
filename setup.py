# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @File: setup.py
# @Author: SWHL
# @Contact: liekkaskono@163.com
from setuptools import setup, find_packages

setup(
    name="img_aug_offline",
    version="0.1",
    author="SWHL",
    author_email="liekkaskono@163.com",
    description="图像离线增强",
    license='Apache-2.0',
    url="https://github.com/SWHL/image_augmentor",
    install_requires=['numpy', 'opencv-python'],
    packages=["img_aug_offline", "img_aug_offline.ops"],  # 用来包含子目录
    entry_points={
        'console_scripts':['img_aug_offline=img_aug_offline.img_aug_offline:main']
    }
)