from hyperlpr import *
import cv2

i = 1


def detectImage():
    path = 'VOC2007/JPEGImages/' + str(i).zfill(6) + ".jpg"
    img = cv2.imread(path)
    print(HyperLPR_PlateRecogntion(img))


if __name__ == '__main__':
    i = int(input('Start With:'))
    while True:
        detectImage()
        i += 1
        input('Enter...')