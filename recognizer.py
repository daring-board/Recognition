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
    while True:
        ie.main()

if __name__=='__main__':
    if len(sys.argv) == 1:
        print('起動モードを選択してください。')
        print('テキストモード: python recognizer.py text')
        print('音声入力モード: python recognizer.py audio')
        print('画像認識モード: python recognizer.py [mode] 1')
        sys.exit()
    lang = threading.Thread(target=lang, name="lang", args=(sys.argv[1],))
    lang.start()
    if len(sys.argv) == 3:
        imge = threading.Thread(target=image,name="img",args=())
        imge.start()
