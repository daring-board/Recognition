import os
import sys
from random import choice
import re
import copy
import dill
from NLP import NLP

class Markov:
    """マルコフ連鎖による文章の学習・生成を行う。

    クラス定数:
    ENDMARK -- 文章の終わりを表す記号
    CHAIN_MAX -- 連鎖を行う最大値
    """
    ENDMARK = '%END%'
    CHAIN_MAX = 30

    def __init__(self):
        """インスタンス変数の初期化。
        self._dic -- マルコフ辞書。 _dic['prefix1']['prefix2'] == ['suffixes']
        self._starts -- 文章が始まる単語の数。 _starts['prefix'] == count
        """
        self._dic = {}
        self._starts = {}

    def add_sentence(self, parts):
        """形態素解析結果partsを分解し、学習を行う。"""
        # 実装を簡単にするため、3単語以上で構成された文章のみ学習する
        if len(parts) < 3:
            return
        # 呼び出し元の値を変更しないように`copy`する
        parts = copy.copy(parts)
        # prefix1, prefix2 には文章の先頭の2単語が入る
        prefix1, prefix2 = parts.pop(0)[0], parts.pop(0)[0]
        # 文章の開始点を記録する
        # 文章生成時に「どの単語から文章を作るか」の参考にするため
        self.__add_start(prefix1)
        # `prefix`と`suffix`をスライドさせながら`__add_suffix`で学習させる
        # 品詞情報は必要ないため、`_`で使わないことを明示する
        # すべての単語を登録したら、最後にENDMARKを追加する
        for suffix, _ in parts:
            self.__add_suffix(prefix1, prefix2, suffix)
            prefix1, prefix2 = prefix2, suffix
        self.__add_suffix(prefix1, prefix2, Markov.ENDMARK)

    def __add_suffix(self, prefix1, prefix2, suffix):
        if prefix1 in self._dic.keys():
            if prefix2 in self._dic[prefix1].keys():
                self._dic[prefix1][prefix2].append(suffix)
            else:
                self._dic[prefix1][prefix2] = [suffix]
        else:
            self._dic[prefix1] = {}
            self._dic[prefix1][prefix2] = [suffix]

    def __add_start(self, prefix1):
        if prefix1 in self._starts.keys():
            self._starts[prefix1] += 1
        else:
            self._starts[prefix1] = 0

    def generate(self, keyword):
        """keywordをprefix1とし、そこから始まる文章を生成して返す。"""
        # 辞書が空である場合はNoneを返す
        if not self._dic:
            return None
        # keywordがprefix1として登録されていない場合、_startsからランダムに選択する
        keys = list(self._starts.keys())
        ch = choice(keys)
        prefix1 = keyword
        if keyword not in self._dic.keys(): return None#prefix1 = ch
        # prefix1をもとにprefix2をランダムに選択する
        prefix2 = choice(list(self._dic[prefix1].keys()))
        # 文章の始めの単語2つをwordsに設定する
        words = [prefix1, prefix2]
        # 最大CHAIN_MAX回のループを回し、単語を選択してwordsを拡張していく
        # ランダムに選択したsuffixがENDMARKであれば終了し、単語であればwordsに追加する
        # その後prefix1, prefix2をスライドさせて始めに戻る
        for _ in range(Markov.CHAIN_MAX):
            suffix = choice(self._dic[prefix1][prefix2])
            if suffix == Markov.ENDMARK:
                break
            words.append(suffix)
            prefix1, prefix2 = prefix2, suffix
        return ''.join(words)

    def load(self, filename):
        """ファイルfilenameから辞書データを読み込む。"""
        with open(filename, 'rb') as f:
            self._dic, self._starts = dill.load(f)

    def save(self, filename):
        """ファイルfilenameへ辞書データを書き込む。"""
        f_path = 'brain/dicts/%s'%filename
        with open(f_path, 'wb') as f:
            dill.dump((self._dic, self._starts), f)

def main():
    nlp = NLP()
    markov = Markov()
    sep = r'[。?？!！ 　]+'
    filename = sys.argv[1]
    dicfile = '{}.dat'.format(filename)
    if os.path.exists(dicfile):
        markov.load(dicfile)
    else:
        with open(filename, 'r', encoding='utf-8') as f:
            sentences = []
            for line in f:
                sentences.extend(re.split(sep, line.strip()))
        for sentence in sentences:
            if sentence:
                markov.add_sentence(nlp.analyze(sentence))
                print('.', end='')
                sys.stdout.flush()
        markov.save(dicfile)
    print('\n')

    while True:
        line = input('> ')
        if not line:
            break
        parts = nlp.analyze(line)
        keyword = next((word for word, part in parts if nlp.is_keyword(part)), '')
        print(markov.generate(keyword))

if __name__ == '__main__':
    main()
