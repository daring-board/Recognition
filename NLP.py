import re
from janome.tokenizer import Tokenizer

class NLP:
    '''
    Natural language processing
    '''
    def __init__(self):
        """コンストラクタ"""
        self.TOKENIZER = Tokenizer()

    def analyze(self, text):
        """文字列textを形態素解析し、[(surface, parts)]の形にして返す。"""
        token = self.TOKENIZER.tokenize(text)
        return [(t.surface, t.part_of_speech) for t in token]

    def is_keyword(self, part):
        """品詞partが学習すべきキーワードであるかどうかを真偽値で返す。"""
        return bool(re.match(r'名詞,(一般|代名詞|固有名詞|サ変接続|形容動詞語幹)', part))
