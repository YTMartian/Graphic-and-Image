# LICENSE PLATE RECOGNITION

JUST A GRAPHIC AND IMAGE PROCESSING HOMEWORK, DETECTING CAR LICENSE PLATE.

# CLIENT

CLIENT IS AN ANDROID APP.
DISPLAY VIDEO STREAM FROM CAMERA, TEH POSITION OF CAR'S LICENSE PLATE AND THE STRING OF IT.

# SERVER

IMPLEMENTED IN PYTHON, INCLUDING FRONT-END WEB FOR ADMINISTRATOR AND PROCESSING ALL DATAS WHICH ARE TRANSMITTED FROM CLIENT.

# SUPPORT

- USE [YOLO: Real-Time Object Detection](https://github.com/qqwweee/keras-yolo3) TO DETECT LICENSE PLATE.
- USE [LabelImg](https://github.com/tzutalin/labelImg) TO LABEL LICENSE PLATE.
- ALSO USE [HyperLPR](https://github.com/zeusees/HyperLPR) TO DETECT LICENSE PLATE.
- DATASET:[CCPD](https://github.com/detectRecog/CCPD)
- PYTHON 3.6.5
- TENSORFLOW-GPU 1.6.0
- KERAS 2.1.5
- CUDA 9.0
- CUDNN v7.0.5
- NUMPY 1.14.3

# HOW TO RUN?
1.run django: python manage.py runserver 0.0.0.0:8000

2.find and change two places of variable "server_ip", (in Android Studio, you can just press "CTRL+SHIFT+F" to find it)change it to your local ipv4 address, you can find it in powershell using command "ipconfig /all"

3.run Client APP
