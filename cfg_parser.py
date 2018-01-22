# -*- coding: utf-8 -*-
class Parse:
    '''　コンストラクタ'''
    def __init__(self):
        self._stack = []

    '''　形態素を複合処理した後のトークン集合を渡す'''
    def parser(self, tokens):
        s_len = self._subj_proc(tokens)
        v_len = self._verb_pred_proc(tokens)
        self._obj_proc(tokens, s_len, v_len)

    '''　主語に対する処理'''
    def _subj_proc(self, tokens):
        # 最初の『は』または『が』の助詞を検索
        s_tokens = []
        for token in tokens:
            s_tokens.append(token)
            if (token.surface == 'は' or token.surface == 'が')\
             and '係助詞' in token.part_of_speech:
                break
        if len(tokens) == len(s_tokens):
            s_tokens = []
        print('主語')
        for token in s_tokens:
            print(token)
        # if len(tokens) == 0:
        #     self._stack.appned('S_end')
        # elif True:
        #     print('Not Implemantation')
        # else:
        #     print('Not Implemantation')
        return len(s_tokens)

    '''　目的語に対する処理'''
    def _obj_proc(self, tokens, s_len, v_len):
        o_tokens = tokens[s_len: -v_len]
        print('\n目的語')
        for token in o_tokens:
            print(token)
        # if len(tokens) == 0:
        #     self._stack.appned('O_end')
        # elif True:
        #     print('Not Implemantation')
        # else:
        #     print('Not Implemantation')

    '''　述語に対する処理'''
    def _verb_pred_proc(self, tokens):
        v_tokens = []
        # 最後の動詞または、形容詞を検索
        for token in reversed(tokens):
            v_tokens.append(token)
            tmp = token.part_of_speech.split(',')
            if '動詞' == tmp[0] or '形容詞' in tmp[0]\
             or '形容動詞' in tmp[1]:
                break
        print('\n述語')
        v_tokens = list(reversed(v_tokens))
        for token in v_tokens:
            print(token)
        # if len(tokens) == 0:
        #     self._stack.appned('V_end')
        # elif True:
        #     print('Not Implemantation')
        # else:
        #     print('Not Implemantation')
        return len(v_tokens)
