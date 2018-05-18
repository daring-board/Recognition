# -*- coding: utf-8 -*-
from itertools import chain
import pycrfsuite
import sklearn
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelBinarizer
import codecs

class CRF:
    ''' コンストラクタ'''
    def __init__(self):
      print('Construct CRF(Conditional Random Fields)')

    def __is_hiragana(self, ch):
        return 0x3040 <= ord(ch) <= 0x309F

    def __is_katakana(self, ch):
        return 0x30A0 <= ord(ch) <= 0x30FF

    def get_character_type(self, ch):
        if ch.isspace():
            return 'ZSPACE'
        elif ch.isdigit():
            return 'ZDIGIT'
        elif ch.islower():
            return 'ZLLET'
        elif ch.isupper():
            return 'ZULET'
        elif self.__is_hiragana(ch):
            return 'HIRAG'
        elif self.__is_katakana(ch):
            return 'KATAK'
        else:
            return 'OTHER'

    def get_character_types(self, string):
        character_types = map(self.get_character_type, string)
        character_types_str = '-'.join(sorted(set(character_types)))

        return character_types_str

    def extract_pos_with_subtype(self, morph):
        idx = morph.index('*')
        return '-'.join(morph[1:idx])

    def word2features(self, sent, i):
        word = sent[i][0]
        chtype = self.get_character_types(sent[i][0])
        postag = self.extract_pos_with_subtype(sent[i])
        features = [
            'bias',
            'word=' + word,
            'type=' + chtype,
            'postag=' + postag,
        ]
        if i >= 2:
            word2 = sent[i-2][0]
            chtype2 = self.get_character_types(sent[i-2][0])
            postag2 = self.extract_pos_with_subtype(sent[i-2])
            iobtag2 = sent[i-2][-1]
            features.extend([
                '-2:word=' + word2,
                '-2:type=' + chtype2,
                '-2:postag=' + postag2,
                '-2:iobtag=' + iobtag2,
            ])
        else:
            features.append('BOS')

        if i >= 1:
            word1 = sent[i-1][0]
            chtype1 = self.get_character_types(sent[i-1][0])
            postag1 = self.extract_pos_with_subtype(sent[i-1])
            iobtag1 = sent[i-1][-1]
            features.extend([
                '-1:word=' + word1,
                '-1:type=' + chtype1,
                '-1:postag=' + postag1,
                '-1:iobtag=' + iobtag1,
            ])
        else:
            features.append('BOS')

        if i < len(sent)-1:
            word1 = sent[i+1][0]
            chtype1 = self.get_character_types(sent[i+1][0])
            postag1 = self.extract_pos_with_subtype(sent[i+1])
            features.extend([
                '+1:word=' + word1,
                '+1:type=' + chtype1,
                '+1:postag=' + postag1,
            ])
        else:
            features.append('EOS')

        if i < len(sent)-2:
            word2 = sent[i+2][0]
            chtype2 = self.get_character_types(sent[i+2][0])
            postag2 = self.extract_pos_with_subtype(sent[i+2])
            features.extend([
                '+2:word=' + word2,
                '+2:type=' + chtype2,
                '+2:postag=' + postag2,
            ])
        else:
            features.append('EOS')

        return features

    def sent2features(self, sent):
        return [self.word2features(sent, i) for i in range(len(sent))]

    def sent2labels(self, sent):
        return [morph[-1] for morph in sent]

    def sent2tokens(self, sent):
        return [morph[0] for morph in sent]

    def bio_classification_report(self, y_true, y_pred):
        lb = LabelBinarizer()
        y_true_combined = lb.fit_transform(list(chain.from_iterable(y_true)))
        y_pred_combined = lb.transform(list(chain.from_iterable(y_pred)))

        tagset = set(lb.classes_) - {'O'}
        tagset = sorted(tagset, key=lambda tag: tag.split('-', 1)[::-1])
        class_indices = {cls: idx for idx, cls in enumerate(lb.classes_)}

        return classification_report(
            y_true_combined,
            y_pred_combined,
            labels = [class_indices[cls] for cls in tagset],
            target_names = tagset,
        )


class CorpusReader(object):
    ''' コンストラクタ'''
    def __init__(self, path):
        with codecs.open(path, encoding='utf-8') as f:
            sent = []
            sents = []
            for line in f:
                if line == '\r\n':
                    sents.append(sent)
                    sent = []
                    continue
                morph_info = line.strip().split('\t')
                sent.append(morph_info)
        train_num = int(len(sents) * 0.9)
        self.__train_sents = sents[:train_num]
        self.__test_sents = sents[train_num:]

    def iob_sents(self, name):
        if name == 'train':
            return self.__train_sents
        elif name == 'test':
            return self.__test_sents
        else:
            return None

if __name__ == '__main__':
    c = CorpusReader('test_data/train_data.txt')
    train_sents = c.iob_sents('train')
    test_sents = c.iob_sents('test')
    crf = CRF()
    print(test_sents[:3])
    X_train = [crf.sent2features(s) for s in train_sents]
    y_train = [crf.sent2labels(s) for s in train_sents]

    X_test = [crf.sent2features(s) for s in test_sents]
    y_test = [crf.sent2labels(s) for s in test_sents]

    trainer = pycrfsuite.Trainer(verbose=False)
    for xseq, yseq in zip(X_train, y_train):
        trainer.append(xseq, yseq)

    trainer.set_params({
        'c1': 1.0,   # coefficient for L1 penalty
        'c2': 1e-3,  # coefficient for L2 penalty
        'max_iterations': 50,  # stop earlier

        # include transitions that are possible, but not observed
        'feature.possible_transitions': True
    })

    trainer.train('brain/specific_representation/model.crfsuite')
    tagger = pycrfsuite.Tagger()
    tagger.open('brain/specific_representation/model.crfsuite')

    # example_sent = test_sents[0]
    # print(' '.join(crf.sent2tokens(example_sent)))
    #
    # print("Predicted:", ' '.join(tagger.tag(crf.sent2features(example_sent))))
    # print("Correct:  ", ' '.join(crf.sent2labels(example_sent)))

    # テストデータ全体を予測
    y_pred = [tagger.tag(xseq) for xseq in X_test]
    print(crf.bio_classification_report(y_test, y_pred))
