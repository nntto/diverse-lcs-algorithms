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


## 実験結果 
XとYをそれぞれ i 倍し、それぞれの j 文字目までの接頭辞付け加えた文字列ペアについて実験を実行した．
実験データが格納された csv ファイルからは，タイムアウトしたデータを手動で取り除いてある．

### $k\in[2..10], n=9i, (i\in[1..10])$
実験データ：`9i_experiment_results_without_timeout.csv`
グラフ：`exp_plt_9i/`

### $k=2, n=9\times i+j$
実験データ：`k=2_9i+j_experiment_results_without_timeout.csv`
グラフ：`exp_plt_k=2/`

### $k=2, n=9\times i + j(j\in{0, 5})$
実験データ：`k=2_9i+5j_experiment_results_without_timeout.csv`
グラフ：`exp_plt_k=2_5j/`

### $k=4, n=9\times i+j$
実験データ：`k=4_9i+j_experiment_results_without_timeout.csv`
グラフ：`exp_plt_k=4/`

### $k=4, n=9\times i + j(j\in{0, 5})$
実験データ：`k=4_9i+5j_experiment_results_without_timeout.csv`
グラフ：`exp_plt_k=4_5j/`

### $k\in[2..10], n=18$
実験データ：`n=18_experiment_results.csv`
グラフ：`exp_plt_n=18/`

### $k\in[2..10], n=27$
実験データ：`n=27_experiment_results.csv`
グラフ：`exp_plt_n=27/`