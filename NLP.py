import re
from janome.tokenizer import Tokenizer
from gensim.models import KeyedVectors
from gensim.models import word2vec
import subprocess
from subprocess import Popen

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
        root_path = '.'
        input_path = '%s/input'%root_path
        output_path = '%s/output'%root_path
        with open('%s/input.csv'%input_path, 'w', encoding='shift-jis') as f:
            f.write('文Id,文\n1,%s\n'%text.strip())
        cmd = 'java -jar -Xmx512M %s/compoundAnalyzer.jar -i %s/input.csv -o %s'%(root_path, input_path, output_path)
        #print(cmd)
        proc = Popen(cmd)
        proc.wait()
        data = [line.strip().split(',') for line in open(output_path+'/input_cw.csv', 'r')][1:]
        print(data)
        data = [(item[1].strip('"'), item[2].strip('"')) for item in data]
        return data

    def is_keyword(self, part):
        """品詞partが学習すべきキーワードであるかどうかを真偽値で返す。"""
        if '複合語-事物-一般' in part:
            return True, part
        else:
            return False, part

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
    print(nlp.analyze('日本経済新聞社によると、関ジャニ∞の渋谷君が千代田区のスペイン村で豪遊した帰りに、六本木ヒルズの無国籍レストランで地中海料理かフランス料理か日本料理か迷ったらしいんだけど。'))
