import random
import cv2
from pathlib import Path
import numpy as np


class Blur:
    def __init__(self, ksize):
        self.kernel_size = ksize

    def process(self, img):
        return cv2.GaussianBlur(img, (self.kernel_size, self.kernel_size), 0)


def salt_pepper_noise(image, prob):
    '''
    添加椒盐噪声
    prob:噪声比例 
    '''
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


def gauss_noise(img, sigma):
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


def save_img(save_path, img):
    cv2.imwrite(save_path, img)


if __name__ == "__main__":
    root_path = Path(__file__).resolve().parent
    im = cv2.imread('assets/Rabbit.jpg')

    params_list = [0, 10, 20, 50, 100]
    for i in params_list:
        blur = gauss_noise(im, i)

        save_path = root_path / 'test_images' / f'gauss_noise_{i}.jpg'
        save_img(str(save_path), blur)

    # blur_0 = Blur(0).process(im)
    # save_img(r'G:\ProgramFiles\image_augmentor-master\test_images\blur_0.jpg', blur_0)
