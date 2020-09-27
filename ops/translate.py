import re
import numpy as np
import cv2

CODE = 'trans'
REGEX = re.compile(r"^" + CODE + "_(?P<x_trans>[-0-9]+)_(?P<y_trans>[-0-9]+)")

class Translate:
    def __init__(self, x_trans, y_trans):
        self.code = CODE + str(x_trans) + '_' + str(y_trans)
        self.x_trans = x_trans
        self.y_trans = y_trans

    def process(self, img):
        M = np.float32([[1, 0, self.x_trans], [0, 1, self.y_trans]])
        return cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))

    @staticmethod
    def match_code(code):
        match = REGEX.match(code)
        if match:
            d = match.groupdict()
            return Translate(int(d['x_trans']), int(d['y_trans']))