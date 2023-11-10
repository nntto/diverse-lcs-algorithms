# 仮想環境を構築

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# 実行例
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
INFO - k-Diverse LCS graph computed.
INFO - Diversity min = 3
```
デバッグモードでの実行コマンド
```bash
python main.py python main.py "ABACB" "BABBCAB" 2 --debug
```

# テストを実行する．

```bash
python -m unittest discover tests
```
