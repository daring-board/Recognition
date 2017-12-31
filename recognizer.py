import sys
import subprocess
import audio_output as ao
from time import sleep
from subprocess import Popen

class LangEngine:
    def listen(self):
        #julius -C main.jconf -dnnconf main.dnnconf
        cmd = 'julius_int\\julius.exe -C julius_int/main.jconf -dnnconf julius_int/main.dnnconf'
        proc = Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        count = 0
        while True:
            line = proc.stdout.readline()
            line = line.decode('sjis')
            if count == 0:
                self.speak('start')
                count += 1
            if 'pass1_best:' in line:
                line = line.replace(' ', '')
                print(line)
                if 'プロセスを終了' in line: break
            if not line and proc.poll() is not None:
                break
        proc.kill()

    def speak(self, txt):
        root_path = 'speaker'
        bin_path = 'speaker/bin'
        txt_path = 'speaker/txt'
        cmd = '%s/open_jtalk.exe '%bin_path
        cmd += '-m %s/mei/mei_normal.htsvoice '%bin_path
        cmd += '-x %s/dic -ow voice/%s.wav %s/%s.txt'%(root_path, txt, txt_path, txt)
        proc = Popen(cmd, stdout=subprocess.PIPE)
        proc.wait()
        print('\nvoice/%s.wav'%txt)
        ao.output('voice/%s.wav'%txt)

if __name__=='__main__':
    lang = LangEngine()
    lang.listen()
    lang.speak('close')
