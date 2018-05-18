# -*- coding: utf-8 -*-
import sys
import random
import subprocess
from time import sleep
from subprocess import Popen

import chat as ch
from weather import Weather
import audio_output as ao
from core import Core

class LangEngine:

    def __init__(self):
        '''
        コンストラクタ　
        : コアモジュールをコンストラクト
        '''
        self.ai = Core('AI')

    def createTmp(self, line, op='def'):
        tmp = 'tmp_%s'%op
        txt_path = 'speaker/txt/%s.txt'%tmp
        line = line.split(':')[1]
        with open(txt_path, 'w') as f:
            f.write(line+'\n')
        return tmp

    def throw_responder(self, count, txt):
#        r_attrs = ['greeting', 'template', 'pattern', 'markov', 'what']
#        r_attrs = ['greeting', 'markov', 'markov', 'what']
#        r_attrs = ['greeting', 'markov']
        r_attrs = ['greeting', 'spec_repre']
#        attr = r_attrs[0] if count == 0 else random.choice(r_attrs[1:])
        attr = r_attrs[0]
        if count != 0:
            attr = r_attrs[1]
        self.ai.configure(attr)
        res = self.ai.dialogue(txt)
        # if res == 'No keyword':
        #     attr = random.choice(r_attrs[1:3])
        #     self.ai.configure(attr)
        #     res = self.ai.dialogue(txt)
        # elif res == 'Unkwon words':
        #     attr = r_attrs[4]
        #     self.ai.configure(attr)
        #     res = self.ai.dialogue(txt)
        res = ':'+res
        print('%s%s'%(attr, res))
        self.speak(self.createTmp(res), 'happy')
        count += 1
        return count

    def main_proc(self, txt, count):
        '''
        return: is_break: {True, False}
        '''
        if '終了' == txt:
            self.speak(self.createTmp(':システムを終了します。'))
            self.speak('close')
            return True, count
        if ('天気予報' in txt) or ('天気を教えて' in txt):
            wt = Weather()
            txt = ':'+wt.weather(txt)
            self.speak(self.createTmp(txt), 'happy')
        else:
            count = self.throw_responder(count, txt)
        return False, count

    def input_audio(self):
        '''
        Method for 対話モード
        '''
        #julius -C main.jconf -dnnconf main.dnnconf
        cmd = 'julius_int\\julius.exe -C julius_int/main.jconf -dnnconf julius_int/main.dnnconf'
        proc = Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.speak('start_intractive', 'happy')
        count = 0
        while True:
            line = proc.stdout.readline()
            line = line.decode('sjis')
            if 'pass1_best:' in line:
                line = line.replace(' ', '')
                if len(line.split(':')[1].strip()) == 0: continue
                line = line.split(':')[1].strip()
                print(line)
                is_break, count = self.main_proc(line, count)
                if is_break: break
            if not line and proc.poll() is not None:
                break
        proc.kill()
        self.ai.save()

    def input_text(self):
        '''
        Method for テキストモード
        '''
        self.speak('start_text', 'happy')
        count = 0
        while True:
            txt = input('>> ')
            is_break, count = self.main_proc(txt, count)
            if is_break: break
        self.ai.save()

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

    def main(self, mode):
        if mode == 'audio':
            self.input_audio()
        else:
            self.input_text()

if __name__=='__main__':
    lang = LangEngine()
    if len(sys.argv) < 2:
        lang.input_audio()
    else:
        lang.input_text()
