# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @File: main.py
import os
import re
import sys
import traceback
from multiprocessing.dummy import Pool
from os.path import isfile

import cv2

from counter import Counter
from ops.blur import Blur
from ops.fliph import FlipH
from ops.flipv import FlipV
from ops.noise import Noise
from ops.rotate import Rotate
from ops.translate import Translate
from ops.zoom import Zoom

EXTENSIONS = ['png', 'jpg', 'jpeg', 'bmp']
WORKER_COUNT = max(os.cpu_count() - 1, 1)
OPERATIONS = [Rotate, FlipH, FlipV, Translate, Noise, Zoom, Blur]

'''
Augmented files will have names matching the regex below, eg

    original__rot90__crop1__flipv.jpg

'''
AUGMENTED_FILE_REGEX = re.compile('^.*(__.+)+\\.[^\\.]+$')

# TODO: 暂时不太明白：'.*\\.png中 \\作用
EXTENSION_REGEX = re.compile(
    '|'.join(['.*\\.' + n + '$' for n in EXTENSIONS]), re.IGNORECASE)

thread_pool = None
counter = None


def build_augmented_file_name(original_name, ops):
    root, ext = os.path.splitext(original_name)
    result = root
    for op in ops:
        result += '_' + op.code
    return result + ext


def work(d, f, op_lists):
    try:
        in_path = os.path.join(d, f)
        for op_list in op_lists:  # 从增强角度来逐一对同一图像进行各种增强操作
            out_file_name = build_augmented_file_name(f, op_list)
            if isfile(os.path.join(d, out_file_name)):
                continue  # 文件已经存在
            img = cv2.imread(in_path)
            for op in op_list:
                img = op.process(img)

            cv2.imwrite(os.path.join(d, out_file_name), img)

        counter.processed()
    except:
        traceback.print_exc(file=sys.stdout)


def process(dir, file, op_lists):
    thread_pool.apply_async(work, (dir, file, op_lists))


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: {} <image directory> <operation> (<operation> ...)'.format(
            sys.argv[0]))
        sys.exit(1)

    image_dir = sys.argv[1]
    if not os.path.isdir(image_dir):
        print('Invalid image directory: {}'.format(image_dir))
        sys.exit(2)

    op_codes = sys.argv[2:]
    op_lists = []
    for op_code_list in op_codes:
        op_list = []
        for op_code in op_code_list.split(','):
            op = None
            for op in OPERATIONS:  # 遍历所有的操作，哪个可以匹配上op_code，则添加进list
                op = op.match_code(op_code)  # 这里op返回的是对应操作的实例对象
                if op:
                    op_list.append(op)
                    break

            if not op:
                print('Unknown operation {}'.format(op_code))
                sys.exit(3)
        op_lists.append(op_list)

    counter = Counter()
    thread_pool = Pool(WORKER_COUNT)
    print('Thread pool initialised with {} worker{}'.format(
        WORKER_COUNT, '' if WORKER_COUNT == 1 else 's'))

    matches = []
    for dir_info in os.walk(image_dir):
        dir_name, _, file_names = dir_info
        print('Processing {}...'.format(dir_name))

        for file_name in file_names:
            if EXTENSION_REGEX.match(file_name):
                if AUGMENTED_FILE_REGEX.match(file_name):
                    counter.skipped_augmented()  # 这里是跳过已经增强过的图像，从图像名来看
                else:
                    process(dir_name, file_name, op_lists)
            else:
                counter.skipped_no_match()

    print("Waiting for workers to complete...")
    thread_pool.close()
    thread_pool.join()

    print(counter.get())
