import math
import os
import ccd_processor as ccd_psr
import wit_processor as wit_psr
import tkinter as tk
from tkinter import filedialog


# 公式计算器
class Calculator:
    def __init__(self, times):
        self._distance_l = 4  # 原公式中的 l
        self._b = 30  # 原公式中的 b
        self._quartz_n = 1.46  # 石英折射率
        self._ccd1_filename = ['ccd11.txt', 'ccd12.txt']
        self._ccd2_filename = ['ccd21.txt', 'ccd22.txt']
        self._wit_filename = ['jiaodu1.txt', 'jiaodu2.txt']
        # self._algorithm_name = ['zbz', 'wts']
        self._algorithm_name = ['wts']
        self._times = times
        ###################################################
        self._ccd1 = ccd_psr.CcdProcessor(name=f'第 {self._times} 次实验CCD1')
        self._ccd2 = ccd_psr.CcdProcessor(name=f'第 {self._times} 次实验CCD2')
        self._wit = wit_psr.WitProcessor()
        self._data_directory_path = str()  # 数据文件目录
        self._ccd_height = []  # ccd数据
        self._wit_angle = []  # wit数据
        self._algorithm_select = str()  # 算法选择
        self._get_n = self.get_n_zbz  # get_n
        ###################################################
        self._result = str()

    # 解析数据
    def _fetch_data(self):
        self._ccd_height = [self._ccd1.get_pos_index(), self._ccd2.get_pos_index()]
        self._wit_angle = self._wit.get_angle()

    # 写入self._result
    def _write_result(self, res):
        self._result += res + '\n'

    # 清空self._result
    def _clear_result(self):
        self._result = str()

    # 保存结果
    def save_res(self, open_file=False):
        if len(self._data_directory_path) == 0:
            raise FileNotFoundError('未选择文件目录！')

        # 完成后提示信息预处理
        if open_file:
            following_msg = '将在稍后打开。'
        else:
            following_msg = '需要自行打开。'

        # 保存
        # result_path = '{directory_path}/result_{algorithm}.txt'.format(directory_path=self._data_directory_path, algorithm=self._algorithm_select)
        result_path = '{directory_path}/result_{times}.txt'.format(directory_path=self._data_directory_path, times=self._times)
        with open(result_path, mode='w') as result_file:
            result_file.write(self._result)

        # 提示信息
        print('结果已保存至 {result_path} {following_msg}'.format(result_path=result_path, following_msg=following_msg))

        if open_file:
            os.system('notepad {result_path}'.format(result_path=result_path))

    # 选择数据文件路径
    def select_data_directory_path(self):
        root = tk.Tk()
        root.withdraw()
        print()  # 空一行
        print(f'选择数据文件目录，可保留窗口，在实验完成后再前往选择文件。（第 {self._times} 次）')
        while len(self._data_directory_path) == 0:  # 防手残
            self._data_directory_path = filedialog.askdirectory(title=f'选择数据文件目录 - 第 {self._times} 次')

    # 计算d
    def get_d(self):
        if len(self._wit_angle) == 0 or len(self._ccd_height) == 0:
            raise FileNotFoundError('未解析数据！')

        theta = (math.fabs(self._wit_angle[1] - self._wit_angle[0])) / 180 * math.pi
        sin_theta = math.sin(theta)
        sin_theta_2 = sin_theta ** 2
        d = self._distance_l * sin_theta * (1 - math.sqrt((1 - sin_theta_2) / (pow(self._quartz_n, 2) - sin_theta_2)))
        return d

    # 获取D
    def get_delta(self):
        if len(self._wit_angle) == 0 or len(self._ccd_height) == 0:
            raise FileNotFoundError('未解析数据！')

        return math.fabs(self._ccd_height[1] - self._ccd_height[0]) * 8e-3

    # 获取n （验证比较用）
    def get_n_zbz(self, delta):
        if len(self._wit_angle) == 0 or len(self._ccd_height) == 0:
            raise FileNotFoundError('未解析数据！')

        theta = (math.fabs(self._wit_angle[1] - self._wit_angle[0])) / 180 * math.pi
        sin_theta = math.sin(theta)
        sin_theta_2 = sin_theta ** 2
        d = self.get_d()
        under_sqrt_frac_denominator = math.pow(1 - (delta - d) / (self._b * sin_theta), 2)  # 根号下分式底部的分母
        n = math.sqrt((1 - sin_theta_2) / under_sqrt_frac_denominator + sin_theta_2)
        return n

    # 获取n
    def get_n_wts(self, delta):
        if len(self._wit_angle) == 0 or len(self._ccd_height) == 0:
            raise FileNotFoundError('未解析数据！')

        fixed_delta = delta - self.get_d()
        theta = (math.fabs(self._wit_angle[1] - self._wit_angle[0])) / 180 * math.pi
        sin_theta = math.sin(theta)
        cos_theta = math.cos(theta)
        the_dis = self._b / cos_theta  # 式子中的l，防混淆用the_dis代替
        beta = math.fabs(math.atan(1 / (the_dis / fixed_delta - math.tan(theta))))
        sin_theta_sub_beta = math.fabs(math.sin(theta - beta))
        n = sin_theta / sin_theta_sub_beta
        return n

    # 获取密度
    def get_rou(self, n):
        if len(self._wit_angle) == 0 or len(self._ccd_height) == 0:
            raise FileNotFoundError('未解析数据！')

        slope = 0.0454  # 斜率
        intercept = 1.3329  # 截距
        return (n - intercept) / slope

    # 选择算法
    def select_algorithm(self, selection='zbz'):
        if selection.lower() == 'zbz':
            self._get_n = self.get_n_zbz
        elif selection.lower() == 'wts':
            self._get_n = self.get_n_wts
        else:
            raise ValueError('Choice error ("zbz" or "wts" but not "{0}")!'.format(selection.lower()))
        self._algorithm_select = selection.lower()

    # 输出四个结果
    def work_out(self):
        if len(self._data_directory_path) == 0:
            raise FileNotFoundError('未选择文件目录！')

        self._wit.set_data_file_path(
            ['{directory}/{filename}'.format(directory=self._data_directory_path, filename=self._wit_filename[0]),
             '{directory}/{filename}'.format(directory=self._data_directory_path, filename=self._wit_filename[1])])

        for algo in self._algorithm_name:
            res_counter = 0
            delta_sum = 0
            rou_sum = 0
            self._clear_result()
            self.select_algorithm(algo)
            # self._write_result('Algorithm: {0}'.format(algo))  # 记录所选算法
            for i in self._ccd1_filename:
                for j in self._ccd2_filename:
                    res_counter += 1
                    self._ccd1.set_data_file_path('{directory}/{filename}'.format(directory=self._data_directory_path, filename=i))
                    self._ccd2.set_data_file_path('{directory}/{filename}'.format(directory=self._data_directory_path, filename=j))
                    self._fetch_data()
                    delta_sum += self.get_delta()
                    rou_sum += self.get_rou(n=self._get_n(delta=self.get_delta()))
                    self._write_result('#-------------{res_counter}-------------#'.format(res_counter=res_counter))
                    self._write_result('[ccd1]: {0}'.format(self._ccd_height[0]))
                    self._write_result('[ccd2]: {0}'.format(self._ccd_height[1]))
                    self._write_result('[wit1]: {:.3f}'.format(self._wit_angle[0]))
                    self._write_result('[wit2]: {:.3f}'.format(self._wit_angle[1]))
                    self._write_result('d: {:.3f}'.format(self.get_d()))
                    self._write_result('D: {:.3f}'.format(self.get_delta()))
                    self._write_result('n: {:.3f}'.format(self._get_n(delta=self.get_delta())))
                    self._write_result('rou: {:.3f}'.format(self.get_rou(n=self._get_n(delta=self.get_delta()))))
            self._write_result('#-------------Average-------------#')
            self._write_result('D on average: {:.3f}'.format(delta_sum / res_counter))
            self._write_result('rou on average: {:.3f}'.format(rou_sum / res_counter))
            self._write_result('#-------------When D Averaged-------------#')
            self._write_result('[wit1]: {:.3f}'.format(self._wit_angle[0]))
            self._write_result('[wit2]: {:.3f}'.format(self._wit_angle[1]))
            self._write_result('n: {:.3f}'.format(self._get_n(delta=delta_sum / res_counter)))
            self._write_result('rou: {:.3f}'.format(self.get_rou(n=self._get_n(delta=delta_sum / res_counter))))
            self.save_res()
