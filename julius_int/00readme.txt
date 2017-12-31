Julius 話し言葉音声認識キット for Windows
(2017/10/12)

音声認識を実行するには，バッチファイル run.bat を実行してください．

このキットに含まれている実行プログラム(Julius)はWindows用のみです．
Juliusを自分でコンパイルする場合は，GitHubから最新のソースコードを
ダウンロードして使用してください．
https://github.com/julius-speech/julius

比較的最近のIntel CPU(AVX2/FMA命令を搭載するもの，おおむね2013年以降の
Core/Xeon CPUは搭載)で，かつ十分な性能(2.5-3GHz程度，2コア以上)がないと
実時間で認識できません．なお，標準の設定ではCPUを2コア使用します．

本キットのモデルは話し言葉音声用です．モデルの詳細については，models
フォルダの 00readme.txt を参照してください．

以上
