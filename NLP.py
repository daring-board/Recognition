import re
from gensim.models import KeyedVectors
from gensim.models import word2vec
import subprocess
from subprocess import Popen
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
from cfg_parser import Parse

class NLP:
    '''
    Natural language processing
    '''
    def __init__(self):
        """コンストラクタ"""
#        self.w2v = KeyedVectors.load_word2vec_format('./brain/vocab/entity_vector.model.bin', binary=True)
        self.w2v = word2vec.Word2Vec.load('./brain/vocab/word2vec.gensim.model')
        # PN Tableを読み込み
        lines = [line.strip() for line in open('brain\dicts\pn_table.csv', 'r', encoding='utf-8')]
        data = [line.split(':') for line in lines]
        self._em_dic = [(item[0], item[1]) for item in data] # word: score

    def analyze(self, text):
        """文字列textを形態素解析し、[(surface, parts)]の形にして返す。"""
        char_filters = [UnicodeNormalizeCharFilter()]
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(text)
        token_filters = [CompoundNounFilter(), POSStopFilter(['記号']), LowerCaseFilter()]
        a = Analyzer(char_filters, tokenizer, token_filters)
        data = [(token.surface, token.part_of_speech) for token in a.analyze(text)]
        return data

    def is_keyword(self, part):
        """品詞partが学習すべきキーワードであるかどうかを真偽値で返す。"""
        print(part)
        if '名詞' in part:
            return True, part
        else:
            return False, part

    def predict_emotion(self, token):
        if not ('名詞' in token.part_of_speech\
         #or '動詞' in token.part_of_speech\
         or '形容詞' in token.part_of_speech): return [], []
        word = token.surface
        if word not in self.w2v.wv: return [], []
        vec = self.w2v.wv[word]
        neg_label, neg_score = [], []
        pos_label, pos_score = [], []
        print(word)
        for fact in self._em_dic:
            vec_neg = self.w2v.wv[fact[0]]
            vec_pos = self.w2v.wv[fact[1]]
            neg = (self.cos_sim(vec, vec_neg) + 1)/2 * 100
            pos = (self.cos_sim(vec, vec_pos) + 1)/2 * 100
            print('%s: %f, %s: %f'%(fact[0], neg, fact[1], pos))
            neg_label.append(fact[0])
            pos_label.append(fact[1])
            neg_score.append(neg)
            pos_score.append(pos)
        label = pos_label + neg_label
        score = pos_score + neg_score
        return label, score

    # cos類似度を計算
    def cos_sim(self, v1, v2):
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    def similar_words(self, keyword):
        """
        keywordに入力された単語と似た単語のリストを返却する
        """
        try:
            similar_rugby_list = self.w2v.most_similar(keyword)
        except:
            return []
        return similar_rugby_list

    def check(self):
        similar_rugby_list = self.w2v.most_similar(u'ラグビー')
        for similar_set in similar_rugby_list:
            print(similar_set[0])
            print(similar_set[1])
        similar_rugby_list = self.w2v.most_similar(u'数学')
        for similar_set in similar_rugby_list:
            print(similar_set[0])
            print(similar_set[1])


import matplotlib.pyplot as plt
import radar_chart as rc
def chart(labels, data):
    labels = ['1.Trust', '2.Joy', '3.Lovely', '4.Disgust', '5.Sorrow' , '6.Angry']
    rc.showRadarChart(labels, data)

if __name__ == '__main__':
    nlp = NLP()
#    print(nlp.analyze('日本経済新聞社によると、関ジャニ∞の渋谷君が千代田区のスペイン村で豪遊した帰りに、六本木ヒルズの無国籍レストランで地中海料理かフランス料理か日本料理か迷ったらしいんだけど。'))
    while True:
        text = input('> ')
        if not text:
            break
        print()
        char_filters = [UnicodeNormalizeCharFilter()]
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(text)
        print('形態素解析')
        for token in tokens:
            print(token)
        token_filters = [CompoundNounFilter()]#, POSStopFilter(['記号']), LowerCaseFilter()]
        analyzer = Analyzer(char_filters, tokenizer, token_filters)
        tokens = analyzer.analyze(text)
        print('\n複合語処理後')
        tmp = []
        for token in tokens:
            print(token)
            tmp.append(token)
        print('\n構文解析 by CFG')
        p = Parse()
        p.parser(tmp)
