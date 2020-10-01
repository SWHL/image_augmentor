import re
import numpy as np
import random

CODE = 'noise'
REGEX = re.compile(r"^" + CODE + "_(?P<var>[.0-9]+)")


class Noise:
    def __init__(self, var):
        self.code = CODE + str(var)
        self.var = var

    def process(self, img):
        return self._gauss_noise(img, self.var)

    @staticmethod
    def _salt_pepper_noise(image, prob):
        """
         
        @params:
        """
        output = np.zeros(image.shape, np.uint8)
        thres = 1 - prob
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                rdn = random.random()
                if rdn < prob:
                    output[i][j] = 0
                elif rdn > thres:
                    output[i][j] = 255
                else:
                    output[i][j] = image[i][j]
        return output

    @staticmethod
    def _gauss_noise(img, sigma):
        """
         
        @params:
        
        """
        temp_img = np.float64(np.copy(img))
        h = temp_img.shape[0]
        w = temp_img.shape[1]
        noise = np.random.randn(h, w) * sigma
        noisy_img = np.zeros(temp_img.shape, np.float64)
        if len(temp_img.shape) == 2:
            noisy_img = temp_img + noise
        else:
            noisy_img[:, :, 0] = temp_img[:, :, 0] + noise
            noisy_img[:, :, 1] = temp_img[:, :, 1] + noise
            noisy_img[:, :, 2] = temp_img[:, :, 2] + noise
        return noisy_img

    @staticmethod
    def match_code(code):
        match = REGEX.match(code)
        if match:
            d = match.groupdict()
            return Noise(float(d['var']))
