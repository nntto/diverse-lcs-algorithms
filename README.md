# 仮想環境を構築

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# 実行例
## 提案手法
実行コマンド：
```bash
python main.py python main.py "ABACB" "BABBCAB" 2
```
実行結果：
```bash
INFO - LCS computed for strings 'ABACB' and 'BABBCAB'
INFO - LCS length = 4
INFO - LCS graph computed.
INFO - LCS set: {'ABAB', 'BACB', 'ABCB'}
INFO - 2-Diverse LCS graph computed.
INFO - 2-diverse LCS set : {('ABAB', 'BACB'), ('BACB', 'ABAB')}
INFO - max hamming distance = 3
INFO - mutual hamming weight matrix computed.
INFO - Diversity min = 3
```
デバッグモードでの実行コマンド
```bash
python main.py "ABACB" "BABBCAB" 2 --debug
```
ログは`logs`ディレクトリに保存されます．
ログファイルには，以下の情報が記録されます．
- 通常実行時のログ
- LCS計算に用いたDPテーブル
- LCSグラフ構築時に用いた，DPテーブルの辺の情報
- イプシロン除去後のLCSグラフ
- 階層化されたLCSグラフ
- max-minになる mutual hamming weight matrix を一つ選んだときの，diverse LCS 集合構築の様子．

## ナイーブな実装
実行コマンド：
```bash
python naive.py BACB ABCB ABAB 2
```
実行結果：
```bash
INFO - Received the following string set: ['BACB', 'ABCB', 'ABAB']
INFO - Received the following value of k: 2
INFO - Minimum diversity: 3
INFO - Minimum diversity set: ('BACB', 'ABAB')
```

# テストを実行する．

```bash
python -m unittest discover tests
```
