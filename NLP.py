import re
from janome.tokenizer import Tokenizer
from gensim.models import KeyedVectors
from gensim.models import word2vec

class NLP:
    '''
    Natural language processing
    '''
    def __init__(self):
        """コンストラクタ"""
        self.TOKENIZER = Tokenizer()
#        self.w2v = KeyedVectors.load_word2vec_format('./brain/vocab/entity_vector.model.bin', binary=True)
        self.w2v = word2vec.Word2Vec.load('./brain/vocab/word2vec.gensim.model')

    def analyze(self, text):
        """文字列textを形態素解析し、[(surface, parts)]の形にして返す。"""
        token = self.TOKENIZER.tokenize(text)
        return [(t.surface, t.part_of_speech) for t in token]

    def is_keyword(self, part):
        """品詞partが学習すべきキーワードであるかどうかを真偽値で返す。"""
        return bool(re.match(r'名詞,(一般|代名詞|固有名詞|サ変接続|形容動詞語幹)', part))

    def similar_words(self, keyword):
        """
        keywordに入力された単語と似た単語のリストを返却する
        """
        similar_rugby_list = self.w2v.most_similar(keyword)
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
    nlp = NLP()
    nlp.check()
