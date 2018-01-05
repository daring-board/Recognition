#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json


def loadingJson(dirpath, f):
    fpath = dirpath + '/' + f
    fj = open(fpath,'r', encoding='utf-8')
    json_data = json.load(fj)
    fj.close()
    return json_data

def output(data, mod):
    with open('Utterance.txt', 'a', encoding='sjis') as f:
        for i in range(len(data['turns'])):
            if mod == "U" and data['turns'][i]['speaker'] == mod:
                f.write(data['turns'][i]['utterance'])
                f.write('\n')
            elif mod == "S" and data['turns'][i]['speaker'] == mod and i != 0:
                f.write(data['turns'][i]['utterance'])
                f.write('\n')
            else:
                continue

if __name__ == "__main__":
    argvs = sys.argv
    _usage = """--
Usage:
    python create_data.py [json] [speaker]
Args:
    [json]: The argument is input directory that is contained files of json that is objective to convert to sql.
    [speaker]: The argument is "U" or "S" that is speaker in dialogue.
""".rstrip()

    if len(argvs) < 3:
        print(_usage)
        sys.exit(0)

    # one file ver
    '''
    fj = open(argvs[1],'r')
    json_data = json.load(fj)
    fj.close()

    output(json_data, mod)
    '''

    # more than two files ver
    branch = os.walk(argvs[1])
    mod = argvs[2]

    for dirpath, dirs, files in branch:
        for f in files:
            json_data = loadingJson(dirpath, f)
            output(json_data, mod)
