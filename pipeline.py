import sys

from collection import pixiv
from detection import face
from conversion import line


def main(target=False):
    print('Get illusts from pixiv.')
    STARTID = 10000000
    pixiv_params = {
        'startid' : STARTID,
        'endid' : STARTID + 5000,
        'min_bookmarks' : 0,
        'output' : 'datasets/raw',
        'target' : target
    }
    c = pixiv.Collector()
    c.get_illusts(**pixiv_params)

    print('Crop anime faces.')
    MODEL = 'detection/models/lbpcascade_animeface.xml'
    crop_params = {
        'input' : 'datasets/raw',
        'output' : 'datasets/face'
    }
    cf = face.CropFace(MODEL)
    cf.crop(**crop_params)

    if target == True:
        print('Select anime faces.')
        sieve_params = {
            'input' : 'datasets/face',
            'output' : 'datasets/X'
        }
        face.sieve_by_hue(**sieve_params)

    print('Convert to line drawing.')
    convert_params = {
        'input' : 'datasets/face',
        'output' : 'datasets/y'
    }
    if target == True:
        convert_params['input'] = 'datasets/X'
    line.convert(**convert_params)


if __name__ == '__main__':
    args = sys.argv
    if args[-1] == '-target':
        main(target=True)
    else:
        main(target=False)
