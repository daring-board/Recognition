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

if __name__ == '__main__':
#    nlp = NLP()
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
