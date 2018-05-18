import random
from configparser import ConfigParser
from datetime import datetime
from NLP import NLP
import chat

class Responder:
    """AIの応答を制御するクラス。
    プロパティ:
    name -- Responderオブジェクトの名前
    """
    def __init__(self, name, nlp):
        """文字列を受け取り、自身のnameに設定する。"""
        self._name = name
        self._nlp = nlp

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
    def response(self, text, parts):
        """文字列textを受け取り、'{text}ってなに？'という形式で返す。"""
        keywords = [word for word, part in parts if self._nlp.is_keyword(part)[0]]
        if len(keywords) == 0:
            return '%sってどういうこと？'%text
        return '{}ってなに？'.format(keywords[0])

class GreetingResponder(Responder):
    """
    挨拶用の応答モジュール
    """
    def __init__(self, name, nlp, dic):
        """コンストラクタ"""
        super().__init__(name, nlp)
        self._dict = dic

    def response(self, text, parts):
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

class TemplateResponder(Responder):
    """AIの応答を制御する思考エンジンクラス。
    登録されたパターンに反応し、関連する応答を返す。
    """
    def __init__(self, name, nlp, dic):
        """コンストラクタ"""
        super().__init__(name, nlp)
        self._dict = dic

    def response(self, text, parts):
        """形態素解析結果partsに基づいてテンプレートを選択・生成して返す。"""
        keywords = [word for word, part in parts if self._nlp.is_keyword(part)[0]]
        count = len(keywords)
        if count > 0:
            if count in self._dict:
                template = random.choice(self._dict[count].split('|'))
                for keyword in keywords:
                    template = template.replace('%noun%', keyword, 1)
                return template
        return chat.getChatWithA3rt(text)

class MarkovResponder(Responder):
    def __init__(self, name, nlp, obj):
        """コンストラクタ"""
        super().__init__(name, nlp)
        self._obj = obj

    def response(self, text, parts):
        """形態素のリストpartsからキーワードを選択し、それに基づく文章を生成して返す。
        キーワードに該当するものがなかった場合はランダム辞書から返す。"""
        words = []
        keywords = [w for w, p in parts if self._nlp.is_keyword(p)[0]]
        print(keywords)
        if len(keywords) == 0:
            ''' 対話候補文を構成するためのキーワードを入力から取得できなかった場合
            '''
            return 'No keyword'
        keyword = random.choice(keywords)
        while self._nlp.similar_words(keyword) == []:
            keyword = random.choice(keywords)
        words = [item[0] for item in self._nlp.similar_words(keyword)]
        words.append(keyword)
        random.shuffle(words)
        print(words)
        for word in words:
            response = self._obj.generate(word)
            if response: break
        # response = self._obj.generate(keyword)
        return response if response else 'Unkwon words'

class PatternResponder(Responder):
    """AIの応答を制御する思考エンジンクラス。
    登録されたパターンに反応し、関連する応答を返す。
    """
    def __init__(self, name, nlp, dic):
        """コンストラクタ"""
        super().__init__(name, nlp)
        self._dict = dic

    def response(self, text, parts):
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


from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
import pycrfsuite
class SpecRepreResponder(Responder):
    """
    AIの応答を制御する思考エンジンクラス。
    固有表現を抽出して、割与えられたラベルを確認する。
    """
    def __init__(self, name, nlp):
        """コンストラクタ"""
        super().__init__(name, nlp)

    def response(self, text, parts):
        char_filters = [UnicodeNormalizeCharFilter()]
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(text)
        # token_filters = [CompoundNounFilter(), POSStopFilter(['記号']), LowerCaseFilter()]
        token_filters = [POSStopFilter(['記号']), LowerCaseFilter()]
        a = Analyzer(char_filters, tokenizer, token_filters)
        data = [str(token) for token in a.analyze(text)]
        tmp = []
        for item in data:
            item = item.split('\t')
            part = item[1].split(',')
            del item[-1]
            item.extend(part)
            print(item)
            tmp.append(item)
        sent = self._nlp.sent2features(tmp)
        tagger = pycrfsuite.Tagger()
        tagger.open('brain/specific_representation/model.crfsuite')
        print(sent)
        y_pred = tagger.tag(sent)
        print(y_pred)
        return text
