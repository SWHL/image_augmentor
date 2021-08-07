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

try:
    from .counter import Counter
    from .ops.blur import Blur
    from .ops.fliph import FlipH
    from .ops.flipv import FlipV
    from .ops.noise import Noise
    from .ops.rotate import Rotate
    from .ops.translate import Translate
    from .ops.zoom import Zoom
except:
    from counter import Counter
    from ops.blur import Blur
    from ops.fliph import FlipH
    from ops.flipv import FlipV
    from ops.noise import Noise
    from ops.rotate import Rotate
    from ops.translate import Translate
    from ops.zoom import Zoom
'''
Augmented files will have names matching the regex below, eg

    original__rot90__crop1__flipv.jpg

'''

EXTENSIONS = ['png', 'jpg', 'jpeg', 'bmp']
WORKER_COUNT = max(os.cpu_count() - 1, 1)

AUGMENTED_FILE_REGEX = re.compile('^.*(__.+)+\\.[^\\.]+$')

# TODO: 暂时不太明白：'.*\\.png中 \\作用
EXTENSION_REGEX = re.compile(
    '|'.join(['.*\\.' + n + '$' for n in EXTENSIONS]), re.IGNORECASE)
OPERATIONS = [Rotate, FlipH, FlipV, Translate, Noise, Zoom, Blur]


class ImgAugOffline(object):
    """对图像离线增强
    目前支持的操作有Rotate, FlipH, FlipV, Translate, Noise, Zoom, Blur
    详情参见https://github.com/SWHL/image_augmentor

    :param object ([type]): [description]
    """
    def __init__(self) -> None:
        self.counter = Counter()
        self.thread_pool = Pool(WORKER_COUNT)

    def __call__(self, image_dir, op_codes: list):
        self.image_dir = image_dir

        if not os.path.isdir(image_dir):
            print('Invalid image directory: {}'.format(image_dir))
            sys.exit(2)

        op_lists = []
        for op_code in op_codes:
            op = None

            # 遍历所有的操作，哪个可以匹配上op_code，则添加进list
            for op in OPERATIONS:
                # 这里op返回的是对应操作的实例对象
                op = op.match_code(op_code)
                if op:
                    op_lists.append(op)
                    break

            if not op:
                print('Unknown operation {}'.format(op_code))
                sys.exit(3)

        print('Thread pool initialised with {} worker{}'.format(
            WORKER_COUNT, '' if WORKER_COUNT == 1 else 's'))

        for dir_info in os.walk(self.image_dir):
            dir_name, _, file_names = dir_info
            print('Processing {}...'.format(dir_name))

            for file_name in file_names:
                if EXTENSION_REGEX.match(file_name):
                    if AUGMENTED_FILE_REGEX.match(file_name):
                         # 这里是跳过已经增强过的图像，从图像名来看
                        self.counter.skipped_augmented()
                    else:
                        process(self.thread_pool, dir_name,
                                file_name, op_lists, self.counter)
                else:
                    self.counter.skipped_no_match()

        print("Waiting for workers to complete...")
        self.thread_pool.close()
        self.thread_pool.join()

        print(self.counter.get())


def build_augmented_file_name(original_name, op):
    root, ext = os.path.splitext(original_name)
    root += '_' + op.code
    return root + ext

def process(thread_pool, dir_name, file, op_lists, counter):
    thread_pool.apply_async(work, (dir_name, file, op_lists, counter))

def work(dir_name, file_name, op_lists, counter):
    try:
        raw_img_path = os.path.join(dir_name, file_name)
        img = cv2.imread(raw_img_path)

        # 从增强角度来逐一对同一图像进行各种增强操作
        for op in op_lists:
            out_file_name = build_augmented_file_name(file_name, op)
            if isfile(os.path.join(dir_name, out_file_name)):
                continue

            img = op.process(img)
            cv2.imwrite(os.path.join(dir_name, out_file_name), img)
        counter.processed()
    except:
        traceback.print_exc(file=sys.stdout)


def main():
    if len(sys.argv) < 3:
        print(f'Usage: {sys.argv[0]} ' \
            '<image directory> <operation> (<operation> ...)')
        sys.exit(1)

    image_dir = sys.argv[1]
    if not os.path.isdir(image_dir):
        print('Invalid image directory: {}'.format(image_dir))
        sys.exit(2)

    op_codes = sys.argv[2:]
    op_lists = []
    for op_code in op_codes:
        op = None

        # 遍历所有的操作，哪个可以匹配上op_code，则添加进list
        for op in OPERATIONS:
            # 这里op返回的是对应操作的实例对象
            op = op.match_code(op_code)
            if op:
                op_lists.append(op)
                break

        if not op:
            print('Unknown operation {}'.format(op_code))
            sys.exit(3)

    counter = Counter()
    thread_pool = Pool(WORKER_COUNT)
    print('Thread pool initialised with {} worker{}'.format(
        WORKER_COUNT, '' if WORKER_COUNT == 1 else 's'))

    for dir_info in os.walk(image_dir):
        dir_name, _, file_names = dir_info
        print('Processing {}...'.format(dir_name))

        for file_name in file_names:
            if EXTENSION_REGEX.match(file_name):
                if AUGMENTED_FILE_REGEX.match(file_name):
                    counter.skipped_augmented()  # 这里是跳过已经增强过的图像，从图像名来看
                else:
                    process(thread_pool, dir_name,
                            file_name, op_lists, counter)
            else:
                counter.skipped_no_match()

    print("Waiting for workers to complete...")
    thread_pool.close()
    thread_pool.join()

    print(counter.get())
