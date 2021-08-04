import re
import cv2

CODE = 'blur'
REGEX = re.compile(r"^" + CODE + "_(?P<ksize>[.0-9]+)")

class Blur:
    def __init__(self, ksize):
        self.code = CODE + str(ksize)
        self.kernel_size = int(ksize)

    def process(self, img):
        return cv2.GaussianBlur(img, (self.kernel_size, self.kernel_size), 0)

    @staticmethod
    def match_code(code):
        match = REGEX.match(code)
        if match:
            d = match.groupdict()
            return Blur(float(d['ksize']))
