# -*- coding: utf-8 -*-
import sys
from time import sleep
import numpy as np
import cv2, os

class ImageEngine():
    '''
    画像処理エンジン
    '''
    def __init__(self):
        print('Construct ImageEngine')
        # Haar-like特徴分類器
        cascadePath = "test_data/haarcascade_frontalface_default.xml"
        self._f_cas = cv2.CascadeClassifier(cascadePath)
        # LBPH
        self._rec = cv2.face.LBPHFaceRecognizer_create()
        self._rec.read('learning/faces.save')
        self._size = (112, 92)
        self._cap = cv2.VideoCapture(0)
        tmp = [line.strip().split(',') for line in open('brain/faces/face_label.csv', 'r')]
        self._face_dic = {int(item[0]): item[1] for item in tmp}

    '''
    デストラクタ：Webカメラを解法する
    '''
    def __del__(self):
        self._cap.release()
#        cv2.destroyAllWindows()

    '''
    Webカメラの画像をキャプチャする
    '''
    def capture(self):
#        print('capture')
        ret, img = self._cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self._f_cas.detectMultiScale(gray, 1.3, 5)
        cood = 10
        imgs = []
        for (x,y,w,h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            imgs.append((gray[y-cood:y+h+cood, x-cood:x+w+cood], (x, y+h+cood)))
        return img, imgs

    '''
    顔データを推測する
    '''
    def predict(self, img):
#        print('prediction')
        img = cv2.resize(img, self._size)
        label, confidence = self._rec.predict(img)
        return label, confidence

    def main(self):
        img, faces = self.capture()
        ret = []
        color = (255, 0, 255)
        for face in faces:
            label, confidence = self.predict(face[0])
            ret.append((label, confidence))
            text = '%s:%d'%(self._face_dic[label], confidence)
            cv2.putText(img, text, face[1], cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)
        cv2.imshow('img', img)
        cv2.waitKey(1000)
        return ret

if __name__=='__main__':
    ie = ImageEngine()
    while True:
        ie.main()
