from NLP import NLP

class Dictionary:
    """
    会話データ登録クラス
    """

    def __init__(self, target):
        """コンストラクタ"""
        self.f_path = 'brain/dic/%s.ini'%target
        lines = [line.strip() for line in open(self.f_path, 'r', encoding='utf-8')]
        self._dict = {l.split('\t')[0]: l.split('\t')[1] for l in lines}
        self._nlp = NLP()

    @staticmethod
    def pattern_to_line(key, phrase):
        """パターンのハッシュを文字列に変換する。"""
        return '{}\t{}'.format(key, '|'.join(phrase))

    @property
    def data(self):
        return self._dict

    def study(self, text):
        """ユーザーの発言textを、形態素partsに基づいてパターン辞書に保存する。"""
        parts = self._nlp.analyze(text)
        for word, part in parts:
            if self._nlp.is_keyword(part):  # 品詞が名詞であれば学習
                # 単語の重複チェック
                # 同じ単語で登録されていれば、パターンを追加する
                # 無ければ新しいパターンを作成する
                duplicated = next((key for key in self._dict.keys() if key == word), None)
                print(duplicated)
                if duplicated:
                    if text not in self._dict[word]:
                        self._dict[word] += '|'+text
                else:
                    self._dict[word] = text
        print(self._dict)

    def save(self):
        """メモリ上の辞書をファイルに保存する。"""
        with open(self.f_path, mode='w', encoding='utf-8') as f:
            for key in self._dict:
                f.write('%s\t%s\n'%(key, self._dict[key]))
