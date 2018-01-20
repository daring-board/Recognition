import sys
import threading
from lang_recognizer import LangEngine
from image_recognizer import ImageEngine

def lang(cmd):
    print('start LangEngine')
    le = LangEngine()
    le.main(cmd)

def image():
    print('start ImageEngine')
    ie = ImageEngine()
    while not event_stop.is_set():
        ie.main()

if __name__=='__main__':
    if len(sys.argv) == 1:
        print('起動モードを選択してください。')
        print('テキストモード: python recognizer.py text')
        print('音声入力モード: python recognizer.py audio')
        print('画像認識モード: python recognizer.py [mode] 1')
        sys.exit()
    event_stop = threading.Event()
    if len(sys.argv) == 3:
        imge = threading.Thread(target=image,name="img",args=())
        imge.start()
    lang(sys.argv[1])
    event_stop.set()
