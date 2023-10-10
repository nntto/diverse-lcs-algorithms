import numpy as np
from termcolor import colored

# 配列の中で異なる値のみ色を変えて表示する
def print_array_diff(expected_array, actual_array):
    # 配列のサイズが異なる場合は，エラーを出力して終了する
    if expected_array.shape != actual_array.shape:
        raise ValueError(
            f"expected_array.shape = {expected_array.shape}, actual_array.shape = {actual_array.shape}"
        )

    # 配列の中で異なる値のインデックスを取得する
    diff = np.where(expected_array != actual_array)

    print()
    print("expected")
    for i in range(expected_array.shape[0]):
        output_row = []
        for j in range(expected_array.shape[1]):
            if (i, j) in zip(*diff):
                output_row.append(colored(str(expected_array[i, j]), "blue"))
            else:
                output_row.append(str(expected_array[i, j]))
        print(" ".join(output_row))

    print("actual")
    # 配列の中で異なる値のみ色を変えて表示する
    for i in range(actual_array.shape[0]):
        output_row = []
        for j in range(actual_array.shape[1]):
            if (i, j) in zip(*diff):
                output_row.append(colored(str(actual_array[i, j]), "red"))
            else:
                output_row.append(str(actual_array[i, j]))
        print(" ".join(output_row))

