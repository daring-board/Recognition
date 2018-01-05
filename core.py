from responder import Responder, WhatResponder, RandomResponder
from responder import GreetingResponder, PatternResponder
from responder import TemplateResponder, MarkovResponder
from dictionary import Dictionary
from NLP import NLP

class Core:
    """コアクラス。

    プロパティ:
    name -- コアの名前
    responder_name -- 現在の応答クラスの名前
    """

    def __init__(self, name):
        """文字列を受け取り、コアインスタンスの名前に設定する。
        Responderインスタンスを作成し、保持する。
        """
        self._name = name
        self._nlp = NLP()
        self._dict = {}
        r_type = 'template'
        self._dict[r_type] = Dictionary(r_type, self._nlp)
        r_type = 'pattern'
        self._dict[r_type] = Dictionary(r_type, self._nlp)
        r_type = 'greeting'
        self._dict[r_type] = Dictionary(r_type, self._nlp)
        r_type = 'what'
        self._dict[r_type] = Dictionary(r_type, self._nlp)
        r_type = 'markov'
        self._dict[r_type] = Dictionary(r_type, self._nlp)


    def configure(self, r_type):
        self.r_type = r_type
        dic = self._dict[r_type]
        if r_type == 'template':
            self._responder = TemplateResponder(r_type, self._nlp, dic.data)
        elif r_type == 'pattern':
            self._responder = PatternResponder(r_type, self._nlp, dic.data)
        elif r_type == 'greeting':
            self._responder = GreetingResponder(r_type, self._nlp, dic.data)
        elif r_type == 'markov':
            self._responder = MarkovResponder(r_type, self._nlp, dic.obj)
        else:
            self._responder = WhatResponder(r_type, self._nlp)

    def dialogue(self, text):
        """ユーザーからの入力を受け取り、Responderに処理させた結果を返す。"""
        parts = self._nlp.analyze(text)
        res = self._responder.response(text, parts)
        print(res)
        self._dict[self.r_type].study(text, parts)
        return res

    def save(self):
        r_type = 'template'
        self._dict[r_type].save()
        r_type = 'pattern'
        self._dict[r_type].save()

    @property
    def name(self):
        """人工無脳インスタンスの名前"""
        return self._name

    @property
    def responder_name(self):
        """保持しているResponderの名前"""
        return self._responder.name
