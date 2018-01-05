import random
from configparser import ConfigParser
from datetime import datetime

class Responder:
    """AIの応答を制御するクラス。
    プロパティ:
    name -- Responderオブジェクトの名前
    """
    def __init__(self, name):
        """文字列を受け取り、自身のnameに設定する。"""
        self._name = name

    def response(self, *args):
        """ユーザーからの入力(text)を受け取り、AIの応答を生成して返す。"""
        pass

    @property
    def name(self):
        """応答オブジェクトの名前"""
        return self._name

class WhatResponder(Responder):
    """
    AIの応答を制御する思考エンジンクラス。
    入力に対して疑問形で聞き返す。
    """
    def response(self, text):
        """文字列textを受け取り、'{text}ってなに？'という形式で返す。"""
        return '{}ってなに？'.format(text)

class GreetingResponder(Responder):
    """
    挨拶用の応答モジュール
    """
    def __init__(self, name, dic):
        """コンストラクタ"""
        super().__init__(name)
        self._dict = dic

    def response(self, text):
        """
        応答ロジック
        """
        sep = 8
        hour = datetime.now().strftime('%H')
        term = int(hour)
        if (term >= 5) and (term < 10):
            '''朝'''
            return self._dict['morning']
        if (term >= 10) and (term < 18):
            '''昼(午後)'''
            section = 'noon'
            if 'こんにち' in text:
                return self._dict[section]
            else: return self._dict[section]
        if (term >= 18) and (term <= 24):
            '''夜'''
            section = 'evening'
            if 'こんばん' in text or '今晩' in text:
                return self._dict[section]
            else:
                return self._dict[section]
        if (term >= 0) and (term < 5):
            '''深夜'''
            section = 'evening%s'
            RESPONSES = [self._dict[section%idx] for idx in range(1, 4)]
            return random.choice(RESPONSES)

class PatternResponder(Responder):
    """AIの応答を制御する思考エンジンクラス。
    登録されたパターンに反応し、関連する応答を返す。
    """
    def __init__(self, name, dic):
        """コンストラクタ"""
        super().__init__(name)
        self._dict = dic

    def response(self, text):
        """ユーザーの入力に合致するパターンがあれば、関連するフレーズを返す。"""
        section = 'patterns'
        for ptn in self._dict.keys():
            if ptn in text:
                res = random.choice(self._dict[ptn].split('|'))
                return res.replace('%match%', text)
        return 'まぁいいや'

class RandomResponder(Responder):
    """
    AIの応答を制御する思考エンジンクラス。
    登録された文字列からランダムなものを返す。

    クラス変数:
    RESPONSES -- 応答する文字列のリスト

    プロパティ:
    name -- RandomResponderオブジェクトの名前
    """
    RESPONSES = ['今日はさむいね', 'チョコたべたい', 'きのう10円ひろった']
    def response(self, _):
        """ユーザーからの入力は受け取るが、使用せずにランダムな応答を返す。"""
        return choice(RandomResponder.RESPONSES)
