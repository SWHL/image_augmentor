from skimage import transform
import re

PREFIX = 'rot'
REGEX = re.compile(r"^" + PREFIX + "_(?P<angle>-?[0-9]+)")  # (?P<name>...) 分组，除了原有的编号外，再指定一个额外的别名

class Rotate:
    def __init__(self, angle):
        self.angle = angle
        self.code = PREFIX + str(angle)

    def process(self, img):
        return transform.rotate(img, -self.angle)

    @staticmethod
    def match_code(code):
        match = REGEX.match(code)
        if match:
            d = match.groupdict()
            return Rotate(int(d['angle']))
