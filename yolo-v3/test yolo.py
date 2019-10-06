from yolo import YOLO, detect_video
from PIL import Image

i = 1

def detectImage(yolo):
    path = 'VOC2007/JPEGImages/' + str(i).zfill(6) + ".jpg"
    img = Image.open(path)
    res = yolo.detect_image(img)
    res.show()

if __name__ == '__main__':
    i = int(input('Start With:'))
    yolo = YOLO()
    while True:
        detectImage(yolo)
        i += 1
        input('Enter...')
    yolo.close_session()