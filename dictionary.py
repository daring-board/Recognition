import os

class Dictionary:
    """
    会話データ登録クラス
    """
    def __init__(self, target, nlp):
        """コンストラクタ"""
        self.target = target
        self.f_path = 'brain/dicts/%s.ini'%target
        self.touch_dicts(target)
        lines = [line.strip() for line in open(self.f_path, 'r', encoding='utf-8')]
        if target == 'template':
            self._dict = {int(l.split('\t')[0]): '' for l in lines}
            for l in lines:
                count, template = l.split('\t')
                if len(self._dict[int(count)]) == 0:
                    self._dict[int(count)] = template
                else:
                    self._dict[int(count)] += '|'+template
        else:
            self._dict = {l.split('\t')[0]: l.split('\t')[1] for l in lines}
        self._nlp = nlp

    def touch_dicts(self, target):
        """辞書ファイルがなければ空のファイルを作成し、あれば何もしない。"""
        f_path = 'brain/dicts/%s.ini'%target
        if not os.path.exists(f_path):
            open(f_path, 'w').close()

    @staticmethod
    def pattern_to_line(key, phrase):
        """パターンのハッシュを文字列に変換する。"""
        return '{}\t{}'.format(key, '|'.join(phrase))

    @property
    def data(self):
        return self._dict

    def study(self, text, parts):
        if self.target == 'patten':
            self.study_pattern(text, parts)
        elif self.target == 'template':
            self.study_template(text, parts)

    def study_template(self, text, parts):
        """形態素のリストpartsを受け取り、
        名詞のみ'%noun%'に変更した文字列templateをself._templateに追加する。
        名詞が存在しなかった場合、または同じtemplateが存在する場合は何もしない。
        """
        template = ''
        count = 0
        for word, part in parts:
            if self._nlp.is_keyword(part):
                word = '%noun%'
                count += 1
            template += word
        if count not in self._dict.keys():
            self._dict[count] = template
        elif template not in self._dict[count]:
            self._dict[count] += '|'+text

    def study_pattern(self, text, parts):
        """ユーザーの発言textを、形態素partsに基づいてパターン辞書に保存する。"""
        for word, part in parts:
            if self._nlp.is_keyword(part):
                duplicated = next((key for key in self._dict.keys() if key == word), None)
                if duplicated:
                    if text not in self._dict[word]:
                        self._dict[word] += '|'+text
                else:
                    self._dict[word] = text

    def save(self):
        """メモリ上の辞書をファイルに保存する。"""
        if self.target == 'template':
            self.save_template()
            return
        with open(self.f_path, mode='w', encoding='utf-8') as f:
            for key in self._dict:
                f.write('%s\t%s\n'%(key, self._dict[key]))

    def save_template(self):
        with open(self.f_path, mode='w', encoding='utf-8') as f:
            for count, templates in self._dict.items():
                templates = templates.split('|')
                for template in templates:
                    f.write('{}\t{}\n'.format(count, template))
