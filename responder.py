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
        self._config = ConfigParser()

    @property
    def config(self):
        return self._config

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
    def __init__(self, name):
        """コンストラクタ"""
        super().__init__(name)
        self._config.read('brain/dic/greeting.ini')

    def response(self, text):
        """
        応答ロジック
        """
        sep = 8
        hour = datetime.now().strftime('%H')
        term = int(hour)
        if (term >= 5) and (term < 10):
            '''朝'''
            return self.config.get('morning', 'w1')
        if (term >= 10) and (term < 18):
            '''昼(午後)'''
            section = 'noon'
            if 'こんにち' in text:
                return self.config.get(section, 'w1')
            else: return self.config.get(section, 'w2')
        if (term >= 18) and (term <= 24):
            '''夜'''
            section = 'evening'
            if 'こんばん' in text or '今晩' in text:
                return self.config.get(section, 'w1')
            else:
                return self.config.get(section, 'w1')
        if (term >= 0) and (term < 5):
            '''深夜'''
            section = 'evening'
            RESPONSES = [self.config.get(section, 'w%d'%idx) for idx in range(2, 5)]
            return random.choice(RESPONSES)

class PatternResponder(Responder):
    """AIの応答を制御する思考エンジンクラス。
    登録されたパターンに反応し、関連する応答を返す。
    """

    def __init__(self, name):
        """コンストラクタ"""
        super().__init__(name)
        self._config.read('brain/dic/pattern.ini')

    def response(self, text):
        """ユーザーの入力に合致するパターンがあれば、関連するフレーズを返す。"""
        section = 'patterns'
        length = int(self.config.get(section, 'len'))
        patterns = [self.config.get(section, 'w%d'%idx) for idx in range(1, length+1)]
        dic = {l.split('\t')[0]: l.split('\t')[1] for l in patterns}
        for ptn in dic.keys():
            if ptn in text:
                return dic[ptn].replace('%match%', text)
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
