import cv2, os
import numpy as np
from time import sleep

def getDatas(path):
    p_list = [path%(idx, idy) for idx in range(1, 43) for idy in range(1, 11)]
    return p_list

def train():
    # トレーニング画像
    train_path = './test_data/att_faces/s%d/%d.pgm'
    p_list = getDatas(train_path)

    # テスト画像
    test_path = './test_data/test'

    # Haar-like特徴分類器
    cascadePath = "test_data/haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascadePath)
    img_list = []
    rab_list = []
    size = (112, 92)
    cood = 10
    for pic in p_list:
        img = cv2.imread(pic)
        img = cv2.resize(img, size)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_list.append(gray)
        if ('41' in pic) or ('42' in pic):
            rab_list.append(1)
        else:
            rab_list.append(0)
    print(dir(cv2.face))

    #   ※ OpenCV3ではFaceRecognizerはcv2.faceのモジュールになります
    # EigenFace
    #recognizer = cv2.face.EigenFaceRecognizer_create()
    # FisherFace
    #recognizer = cv2.face.FisherFaceRecognizer_create()
    # LBPH
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    recognizer.train(img_list, np.array(rab_list))
    recognizer.save('learning/faces.save')
    pred_paths = [
        'test_data/mahoto_glass/11.pgm',
        'test_data/mahoto_glass/20.pgm',
        'test_data/mahoto_noglass/11.pgm',
        'test_data/mahoto_noglass/14.pgm',
        'test_data/faceData/2003/09/02/img_38.0.ppm',
        'test_data/faceData/2003/09/02/img_44.0.ppm'
    ]
    for pred_pic in pred_paths:
        img = cv2.imread(pred_pic)
        img = cv2.resize(img, size)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        label, confidence = recognizer.predict(gray)
        cv2.imshow("test image", img)
        print('label: %s, confidence: %s'%(str(label), str(confidence)))
        cv2.waitKey(3000)

def faceCapture():
    face_cascade = cv2.CascadeClassifier('test_data/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    count = 1
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        cood = 10
        for (x,y,w,h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            dst_img = img[y-cood:y+h+cood, x-cood:x+w+cood]
            cv2.imshow('img',img)
            cv2.imshow('sub_img%d'%count,dst_img)
            cv2.imwrite('test_data/mahoto/%d.pgm'%count, dst_img)
            print(count)
            count += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        sleep(0.5)
    cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    arg = sys.argv[1]
    if arg == 'cap':
        faceCapture()
    else:
        train()
