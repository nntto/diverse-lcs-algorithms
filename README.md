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
python main.py "ABACB" "BABBCAB" 2
```

出力結果：
```bash
lcs_length = 4
lcs_count = 3
min_diversity = 3
```

デバッグモードでの実行コマンド
```bash
python main.py "ABACB" "BABBCAB" 2 --debug-level debug
```

## ナイーブな実装
実行コマンド：
```bash
python naive.py "ABACB" "BABBCAB" 2
```
実行結果：
```bash
lcs_length = 4
lcs_count = 3
min_diversity = 3
```

# 実験
実行コマンド：
```bash
./exp.sh
```

- 出力ファイル
  - `experiment.txt`: 実験のログ．
  - `expertiment.csv`: 実験結果．タイムアウトした場合の結果も含むので注意．
  - `./exp_plt/`: 実験結果のグラフ．

