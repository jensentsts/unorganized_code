# ccd_processor.py：CCD数据处理器
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import filter


class CcdProcessor:
    def __init__(self, name='CCD_unordered'):
        self._gauss_filter_half_len = 5
        self._gauss_filter_s = 5
        ###################################################
        self._file_path = []
        self._file_amount = 0
        self._data = []
        self._filtered_data = []
        self._data_processed = False
        self.name = name
        ###################################################

    # 读取数据
    def _read_data(self, path):
        new_file_data = []
        self._data_processed = False
        with open(path) as f:
            # read file
            while True:
                line = f.readline()
                if not line:
                    break
                if int(line) != 0:
                    new_file_data += [int(line)]
                else:
                    new_file_data += [3960]
        self._data += [new_file_data]

    # 处理数据
    def _data_process(self):
        if self._data_processed:
            return

        self._filtered_data = self._data[0]
        # 标记
        self._data_processed = True

    # 获取最低点的下标（推荐调试用）
    def get_min_height_index(self):
        if not self._data_processed:
            return 0
        min_index = 0
        min_height = 99999
        for index, val in enumerate(self._filtered_data):
            if index <= 20 or index >= len(self._filtered_data) - 20:
                continue
            if val < min_height:
                min_index = index
                min_height = val
        return min_index

    # 绘制折线图
    def show_plot(self, show_data=False):
        if self._file_amount == 0:
            raise FileNotFoundError('未选择文件！')

        self._data_process()
        x = range(0, len(self._filtered_data))
        if show_data:
            for i in self._data:
                plt.plot(x, i)
                plt.show()
        y = self._filtered_data
        plt.plot(x, y)
        plt.show()

    # 获取最低点位置（物理）
    def get_pos_index(self):
        if self._file_amount == 0:
            raise FileNotFoundError('未选择文件！')

        self._data_process()
        return self.get_min_height_index()

    # 选择文件路径并读取数据
    def select_file_path(self):
        self._data = []
        root = tk.Tk()
        root.withdraw()
        self._file_path = filedialog.askopenfilenames(title='为 {name} 选择数据文件'.format(name=self.name))
        self._file_amount = len(self._file_path)
        for path in self._file_path:
            self._read_data(path)
        self._data_process()

    # 设置数据文件路径并读取数据
    def set_data_file_path(self, path):
        if not type(path) == str:
            return
        self._data = []
        self._file_path = path
        self._file_amount = 1
        self._read_data(self._file_path)
        self._data_process()

    # 文件的数量
    def get_file_amount(self):
        return self._file_amount
