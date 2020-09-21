import re
import cv2

PREFIX = 'rot'
REGEX = re.compile(r"^" + PREFIX + "_(?P<angle>-?[0-9]+)")  # (?P<name>...) 分组，除了原有的编号外，再指定一个额外的别名


class Rotate:
    def __init__(self, angle):
        self.angle = angle
        self.code = PREFIX + str(angle)

    def process(self, img):
        rows, cols, _ = img.shape
        M = cv2.getRotationMatrix2D(((cols-1)/2.0, (rows-1)/2.0), self.angle, 1)
        dst = cv2.warpAffine(img, M, (cols, rows))
        return dst

    @staticmethod
    def match_code(code):
        match = REGEX.match(code)
        if match:
            d = match.groupdict()
            return Rotate(int(d['angle']))
