import sys
import os
import glob
import shutil
import cv2
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sys.path.append('.')
from util.utils import set_io_dir


class CropFace:
    def __init__(self, model):
        if not os.path.isfile(model):
            raise IOError(model, 'not found')
        self.model = cv2.CascadeClassifier(model)

    def crop(self, input, output):
        input, output = set_io_dir(input, output)

        illusts = glob.glob(os.path.join(input, '*.png'))

        for illust in illusts:
            root, ext = os.path.splitext(illust)
            img = cv2.imread(illust, cv2.IMREAD_COLOR)
            if isinstance(img, type(None)):
                continue
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            faces = self.model.detectMultiScale(gray)
            for suffix, (x, y, w, h) in enumerate(faces):
                face = img[y:y+h, x:x+w]
                file_name = os.path.basename('{0}_{1}.png'.format(root, suffix))
                cv2.imwrite(os.path.join(output, file_name), face)
                print('DONE: %s' % file_name)


def sieve_by_hue(input, output):
    input, output = set_io_dir(input, output)

    faces = glob.glob(os.path.join(input, '*.png'))

    median_dist = []
    for face in faces:
        img = cv2.imread(face, cv2.IMREAD_COLOR)
        if isinstance(img, type(None)):
            faces.remove(face)
            continue
        height = img.shape[0]
        hair_zone = img[:int(height*0.2)]
        hsv = cv2.cvtColor(hair_zone, cv2.COLOR_BGR2HSV)
        median = np.median(hsv[:,:,0])
        median_dist.append(median)

    dist = np.array(median_dist)
    std = np.std(median_dist)
    mean = np.mean(median_dist)
    selected = [i for i in np.where((mean-std<dist) & (dist<mean+std))[0]]

    for i in selected:
        shutil.copyfile(faces[i], os.path.join(output, os.path.basename(faces[i])))

    sns.distplot(median_dist)
    plt.savefig('Hue_dist.png')
