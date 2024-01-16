#!/bin/bash

# 実験データの設定
X="ABCBAEEDD" # 9文字
Y="ABABCDDEE" # 9文字

# 結果を保存するためのファイル
results_file="experiment_results.txt"

# タイムアウト時間の設定
timeout=300

# ファイルの初期化
echo "Experiment Results" > $results_file
echo "==================" >> $results_file

# main.pyとnaive.pyの両方で各文字列ペアについて実験を実行
# XとYをそれぞれ i 倍した文字列を用意し、それぞれの文字列ペアについて実験を実行する
for i in {1..10}
do
    for k in {2..5}
    do
        # 文字数 n は，XとYの文字数の合計の i 倍
        echo "n = 9*$i = $((9 * $i)), k = $k" >> $results_file
        echo "n = 9*$i = $((9 * $i)), k = $k"

        # 文字列ペアの作成
        str_X=$(printf "%0.s$X" $(seq 1 $i))
        str_Y=$(printf "%0.s$Y" $(seq 1 $i))
        str_pair="$str_X $str_Y"
        
        echo "Testing with string pair: $str_pair" >> $results_file
        echo "Testing with string pair: $str_pair"

        # main.pyの実行
        echo "Running main.py..." >> $results_file
        echo "Running main.py..."
        # 両方をログファイルに書き込む
        /usr/bin/time -l timeout $timeout python main.py $str_pair $k 2>>$results_file | tee -a $results_file

        # naive.pyの実行
        echo "Running naive.py..." >> $results_file
        echo "Running naive.py..."
        /usr/bin/time -l timeout $timeout python naive.py $str_pair $k 2>>$results_file | tee -a $results_file

        echo "---------------------------------" >> $results_file
    done
done

echo "Experiment completed. Results are in $results_file"

python exp_resuluts_txt2csv.py $results_file
