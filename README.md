# Recognition
## Project Zero

## Requirements
pya3rt
pyaudio
janome
gensim
dill

## Referrence
* http://sandmark.hateblo.jp/entry/2017/10/14/003000
* http://myuon-myon.hatenablog.com/entry/20120723/1343009359
* http://julius.osdn.jp/
* https://qiita.com/mkgask/items/0bf9c26dc96e7b0b45ac
* https://a3rt.recruit-tech.co.jp/product/talkAPI/
* http://weather.livedoor.com/weather_hacks/webservice
* http://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/

## Usage
usage: python recognizer.py [option]  
example: python recognizer.py 0

> ### description
> Variable [option] is None or Anything.  
> If [option] is None then recognizer.py run with intractive mode.  
> And if [option] specified anything value then recognizer.py run with text mode.

## Comment
2018/01/17  
形態素解析後の単語を使用してマルコフ連鎖の辞書へ単語を登録していたが、
形態素解析の後に名詞の複合処理を追加してマルコフ連鎖の辞書へ単語登録する  
ように変更した。
その結果、辞書内から助詞が多数失われており、対話候補文が単語の羅列のように  
なってしまった。

2018/01/24
word2vecの以下のモデルは単語本体の意味を学習しているのではなく、
文中で使用される位置や品詞として周囲の単語との並びを学習している。
./brain/vocab/word2vec.gensim.model

## Next Target
* 強化学習により、行動を選択して対話を行う。  
* 天気予報やニュースを取得して、情報をユーザーに提供する。  

## History
* 2018/01/12
```
D:\Recognition>py recognizer.py 1
>> こんばんわ
こんな遅くに何やってるの？
:こんな遅くに何やってるの？
>> プログラムを書いてるの
プログラムを書いたことないです
:プログラムを書いたことないです
>> 一緒に書きますか？
一緒に楽しんでるんです
:一緒に楽しんでるんです
>> 会話楽しいよね。
ジャムはいちごが好きですね
:ジャムはいちごが好きですね
>> 突然ジャムの話ですか
ジャムってなに？
:ジャムってなに？
>> パンに塗る食べ物だよ
パンはしょっぱいですか
:パンはしょっぱいですか
>> しょっぱくないです。
しょっぱくないです。ってどういうこと？
:しょっぱくないです。ってどういうこと？
>> 美味しいってことです。
美味しいってことです。ってどういうこと？
:美味しいってことです。ってどういうこと？
>> 怒ってるの？
調子が出てないな
:調子が出てないな
>> なるほど。もう寝ますか？
なるほど。もう寝ますか？ってどういうこと？
:なるほど。もう寝ますか？ってどういうこと？
>> 寝るのは、嫌なんですね
嫌なんですよ
:嫌なんですよ
>> 了解です。もっとお話ししましょう！
効率が悪いです
:効率が悪いです
>>
```

* 2018/01/13
```
>> こんばんわ
こんな遅くに何やってるの？
greeting:こんな遅くに何やってるの？
>> プログラムを書いています。
プログラムを書いたことないかも
markov:プログラムを書いたことないかも
>> あなた自身がプログラムだからね
あなたって嫌なんや
markov:あなたって嫌なんや
>> じゃあ、名前を教えてください。
名前はゼロです
markov:名前はゼロです
>> ゼロ、今日もよろしく！
None
まぁいいや
pattern:まぁいいや
>> あなたって言われたの結構怒っていたのね
あなたのことを考えてるのです
markov:あなたのことを考えてるのです
>> ありがとう！
None
どういたしまして
template:どういたしまして
>> 私もゼロのことをよく考えていますよ
私ともっとおしゃべりしましょうか
markov:私ともっとおしゃべりしましょうか
>> いいですね、何のお話しますか？
何歳に見えようです
markov:何歳に見えようです
>> 15歳ぐらいですか？
None
秘密です
template:秘密です
>>
```

* 感情極性  
嫌悪:信頼
憂い:喜び
怒り:愛しい
