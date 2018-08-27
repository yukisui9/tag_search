import sys
import os
import glob
import cv2

sys.path.append('../')
from util.utils import set_io_dir


def convert(input, output):
    input, output = set_io_dir(input, output)

    illusts = glob.glob(os.path.join(input, '*.png'))

    for suffix, illust in enumerate(illusts):
        root, ext = os.path.splitext(illust)
        img = cv2.imread(illust, cv2.IMREAD_COLOR)
        if isinstance(img, type(None)):
            continue
        blur = cv2.GaussianBlur(img, (3,3), 0)
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        bin = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 8)
        file_name = '{0}_{1}.png'.format(root, suffix)
        cv2.imwrite(os.path.join(output, file_name), img)
        print('DONE: %s' % file_name)
