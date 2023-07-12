# wit_processor.py：角度传感器数据处理器
import tkinter as tk
from tkinter import filedialog


class WitProcessor:
    def __init__(self):
        self._file_path = []
        self._data = []

    # 获取角度
    def get_angle(self):
        if self.get_file_amount() == 0:
            raise FileNotFoundError('未选择文件！')

        res = []
        for index, path in enumerate(self._file_path):
            self._data = []
            with open(path) as f:
                # read file
                last_line = str()
                while True:
                    line = f.readline()
                    if not line:
                        break
                    temp = line.split(':')
                    if temp[0] == 'angle':
                        last_line = temp[1]
                        break
                # data procession
                data_part = last_line.split()
                for val in data_part:
                    self._data += [float(val)]
            # data restore
            if self._data[2] < 0:
                self._data[2] += 360  # 修正负数，防止后面出现问题
            res += [self._data[2]]
        return res

    # 选择路径
    def select_file_path(self):
        root = tk.Tk()
        root.withdraw()
        self._file_path = filedialog.askopenfilenames(title='选择wit数据文件路径')

    # 设置数据文件路径
    def set_data_file_path(self, path):
        if not type(path) == list:
            return

        self._file_path = path

    # 文件的数量
    def get_file_amount(self):
        return len(self._file_path)
