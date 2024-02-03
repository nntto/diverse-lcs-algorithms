#!/bin/bash

# Pipeのエラーステータスを確実に取得するためにpipefailを設定
set -o pipefail

# 実験データの設定
X="ABCBAEEDD" # 9文字
Y="ABABCDDEE" # 9文字

# 結果を保存するためのファイル
results_file="experiment_results.txt"

# タイムアウト時間の設定
timeout=1000

# ファイルの初期化
echo "Experiment Results" > $results_file
echo "==================" >> $results_file

# main.pyとnaive.pyの両方で各文字列ペアについて実験を実行
# XとYをそれぞれ i 倍した文字列を用意し、それぞれの文字列ペアについて実験を実行する
for k in {2..10}
do
    skip_main=false
    skip_naive=false
    for i in {1..10}
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

        if [ "$skip_main" = false ]; then
            # main.pyの実行
            echo "Running main.py..." >> $results_file
            echo "Running main.py..."
            /usr/bin/time -l timeout $timeout python main.py $str_pair $k 2>>$results_file | tee -a $results_file
            exit_status_main=$?
            if [ $exit_status_main -eq 124 ]; then
                echo "Timeout occurred for n=$((9 * $i)), k=$k" >> $results_file
                skip_main=true
            fi
        else 
            echo "Skipping main.py..." >> $results_file
            echo "Skipping main.py..."
        fi

        if [ "$skip_naive" = false ]; then
            # naive.pyの実行
            echo "Running naive.py..." >> $results_file
            echo "Running naive.py..."

            /usr/bin/time -l timeout $timeout python naive.py $str_pair $k 2>>$results_file | tee -a $results_file
            exit_status_naive=$?
            if [ $exit_status_naive -eq 124 ]; then
                echo "Timeout occurred for n=$((9 * $i)), k=$k" >> $results_file
                skip_naive=true
            fi
        else 
            echo "Skipping naive.py..." >> $results_file
            echo "Skipping naive.py..."
        fi


        echo "---------------------------------" >> $results_file
    done
done

echo "Experiment completed. Results are in $results_file"

python exp_results_txt2csv.py $results_file
python exp_plot.py experiment_results.csv    
