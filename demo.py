# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @File: demo.py
# @Author: SWHL
# @Contact: liekkaskono@163.com
from img_aug_offline import ImgAugOffline


img_auger = ImgAugOffline()

img_auger(r'E:\PythonProjects\image_augmentor\images',
          ['fliph', 'flipv'])