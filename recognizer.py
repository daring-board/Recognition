# -*- coding: utf-8 -*-
import sys
import random
import subprocess
from time import sleep
from subprocess import Popen

import chat as ch
import weather as wt
import audio_output as ao
from core import Core

class LangEngine:

    def createTmp(self, line, op='def'):
        tmp = 'tmp_%s'%op
        txt_path = 'speaker/txt/%s.txt'%tmp
        line = line.split(':')[1]
        with open(txt_path, 'w') as f:
            f.write(line+'\n')
        return tmp

    def throw_responder(self, ai, count, txt):
        r_attrs = ['greeting', 'template', 'pattern', 'markov', 'what']
        attr = r_attrs[0] if count == 0 else random.choice(r_attrs[1:])
        ai.configure(attr)
        txt = ':'+ai.dialogue(txt)
        print(txt)
        self.speak(self.createTmp(txt), 'happy')
        count += 1
        return count

    def input_audio(self):
        #julius -C main.jconf -dnnconf main.dnnconf
        cmd = 'julius_int\\julius.exe -C julius_int/main.jconf -dnnconf julius_int/main.dnnconf'
        proc = Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ai = Core('AI')
        self.speak('start_intractive', 'happy')
        count = 0
        while True:
            line = proc.stdout.readline()
            line = line.decode('sjis')
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
                    self.throw_responder(ai, count, line)
                    count += 1
            if not line and proc.poll() is not None:
                break
        self.speak(self.createTmp(':システムを終了します。'))
        proc.kill()
        ai.save()
        self.speak('close')

    def input_text(self):
        ai = Core('AI')
        self.speak('start_text', 'happy')
        count = 0
        while True:
            txt = input('>> ')
            if '終了' == txt:
                self.speak(self.createTmp(':システムを終了します。'))
                self.speak('close')
                break
            if '天気予報' in txt:
                txt = ':'+wt.weather()
                self.speak(self.createTmp(txt))
            else:
                count = self.throw_responder(ai, count, txt)
        ai.save()
            # sleep(2)
            # self.speak('next', 'happy')

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
    if len(sys.argv) < 2:
        lang.input_audio()
    else:
        lang.input_text()
