# filter.py：过滤器
import numpy as np


# 高斯函数
def _gauss_func(x, u=0, s=1.5):
    return 1 / (s * np.sqrt(2 * np.pi)) * np.exp(-((x - u) ** 2) / (2 * s ** 2))


# 兼容
def do_nothing(data, data_length):
    if data_length != 0:
        return data[0]
    return []


# 卡尔曼滤波
def kalman_filter(data, data_length):
    res = [0] * data_length

    return data_length


# 均值滤波
def average_filter(data, data_length):
    res = [0] * data_length
    for i in data:
        for j, val in enumerate(i):
            res[j] += val / len(data)
    return res


# 高斯滤波
def gaussian_filter(data, data_length, gauss_half_len=36, s=60):
    res = [0] * data_length
    # 前段数据
    """
    for i in range(0, gauss_half_len + 1):
        res[i] = (np.array(data[0: gauss_half_len * 2 + 1]) * _gauss_func(np.arange(-i, gauss_half_len * 2 + 1 - i))).sum()
    """
    res[0: gauss_half_len] = data[0: gauss_half_len]
    # 中段数据
    gauss_array = _gauss_func(np.arange(-gauss_half_len, 1 + gauss_half_len), s=s)
    gauss_array /= gauss_array.sum()
    for i in range(gauss_half_len, data_length - gauss_half_len):
        res[i] = (np.array(data[(i - gauss_half_len): (i + gauss_half_len + 1)]) * gauss_array).sum()
    # 末段数据
    """
    for i in range(0, gauss_half_len + 1):
        res[data_length - gauss_half_len - 1 + i] = (np.array(data[data_length - gauss_half_len * 2 - 1: data_length]) * _gauss_func(np.arange(-gauss_half_len - i, 1 + gauss_half_len - i))).sum()
    """
    res[data_length - gauss_half_len: data_length] = data[data_length - gauss_half_len: data_length]

    return res
