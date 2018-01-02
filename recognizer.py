import sys
import subprocess
from time import sleep
from subprocess import Popen

import chat as ch
import weather as wt
import audio_output as ao

class LangEngine:
    queue = []

    def createTmp(self, line):
        tmp = 'tmp'
        txt_path = 'speaker/txt/%s.txt'%tmp
        line = line.split(':')[1]
        with open(txt_path, 'w', encoding='sjis') as f:
            f.write(line+'\n')
        return tmp

    def listen(self):
        #julius -C main.jconf -dnnconf main.dnnconf
        cmd = 'julius_int\\julius.exe -C julius_int/main.jconf -dnnconf julius_int/main.dnnconf'
        proc = Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        count = 0
        while True:
            line = proc.stdout.readline()
            line = line.decode('sjis')
            if count == 0:
                self.speak('start', 'happy')
                count += 1
            if 'pass1_best:' in line:
                line = line.replace(' ', '')
                if 'プロセスを終了' in line: break
                if len(line.split(':')[1].strip()) == 0: continue
                print(line)
                #self.speak(self.createTmp(line))
                if '天気を教えて' in line or '天気予報' in line:
                    txt = ':'+wt.weather()
                    self.speak(self.createTmp(txt), 'happy')
                else:
                    txt = ':'+ch.getChat(line)
                    self.speak(self.createTmp(txt), 'happy')
            if not line and proc.poll() is not None:
                break
        self.speak(self.createTmp(':システムを終了します。'))
        proc.kill()

    '''
    emotion: Can specifiy following list
            [normal, angry, bashful, happy, sad]
    '''
    def speak(self, txt, emotion='neutral'):
        root_path = 'speaker'
        bin_path = 'speaker/bin'
        txt_path = 'speaker/txt'
        cmd = '%s/open_jtalk.exe '%bin_path
        cmd += '-m %s/tohoku/tohoku-f01-%s.htsvoice '%(bin_path, emotion)
        cmd += '-x %s/dic -ow voice/%s.wav %s/%s.txt'%(root_path, txt, txt_path, txt)
        proc = Popen(cmd, stdout=subprocess.PIPE)
        proc.wait()
        ao.output('voice/%s.wav'%txt)

if __name__=='__main__':
    lang = LangEngine()
    lang.listen()
    lang.speak('close')
