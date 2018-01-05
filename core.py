from responder import Responder, WhatResponder, RandomResponder
from responder import GreetingResponder, PatternResponder
from dictionary import Dictionary

class Core:
    """コアクラス。

    プロパティ:
    name -- コアの名前
    responder_name -- 現在の応答クラスの名前
    """

    def __init__(self, name):
        """文字列を受け取り、コアインスタンスの名前に設定する。
        ’What' Responderインスタンスを作成し、保持する。
        """
        self._name = name
        self._dict = Dictionary('pattern')
        self._responder = PatternResponder('Pattern', self._dict.data)
#        self._responder = GreetingResponder('Greeting', Dictionary('greeting'))
#        self._responder = RandomResponder('Random')

    def dialogue(self, text):
        """ユーザーからの入力を受け取り、Responderに処理させた結果を返す。"""
        res = self._responder.response(text)
        print(res)
        self._dict.study(text)
        return res

    def save(self):
        self._dict.save()

    @property
    def name(self):
        """人工無脳インスタンスの名前"""
        return self._name

    @property
    def responder_name(self):
        """保持しているResponderの名前"""
        return self._responder.name
