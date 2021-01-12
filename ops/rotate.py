import re
import cv2

PREFIX = 'rot'
REGEX = re.compile(r"^" + PREFIX + "_(?P<angle>-?[0-9]+)")  # (?P<name>...) 分组，除了原有的编号外，再指定一个额外的别名


class Rotate:
    def __init__(self, angle):
        self.angle = angle
        self.code = PREFIX + str(angle)

    def process(self, img):
        height, width = img.shape[:2]
        image_center = (width/2, height/2)

        rotation_mat = cv2.getRotationMatrix2D(image_center, -self.angle, 1.)

        # rotation calculates the cos and sin, taking absolutes of those.
        abs_cos = abs(rotation_mat[0,0]) 
        abs_sin = abs(rotation_mat[0,1])

        # find the new width and height bounds
        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        # subtract old image center (bringing image back to origo) and adding the new image center coordinates
        rotation_mat[0, 2] += bound_w/2 - image_center[0]
        rotation_mat[1, 2] += bound_h/2 - image_center[1]

        # rotate image with the new bounds and translated rotation matrix
        rotated_img = cv2.warpAffine(img, rotation_mat, (bound_w, bound_h))
        return rotated_img

    @staticmethod
    def match_code(code):
        match = REGEX.match(code)
        if match:
            d = match.groupdict()
            return Rotate(int(d['angle']))
