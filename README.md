# Recognition

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
