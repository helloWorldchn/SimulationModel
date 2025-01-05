import control as ctrl
import matplotlib.pyplot as plt
import numpy as np


class FrequencyDomain:

    def __init__(self, numeratorOri="100", denominatorOri="0.001 0.11 1 0") -> None:
        """
        3 频域仿真设计 伯德(Bode)图和奈奎斯特(Nyquist)曲线图
        :param numeratorOri: 分子字符串
        :param denominatorOri: 分母字符串
        """
        self.numeratorOri = numeratorOri  # 分子字符串
        self.denominatorOri = denominatorOri  # 分母字符串

    def frequencyDomain(self):
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False
        # 定义传递函数
        # numerator = [100]  # 分子系数
        # denominator = [0.001, 0.11, 1, 0]  # 分母系数
        numerator = [float(num) for num in self.numeratorOri.split()]  # 分子系数
        denominator = [float(num) for num in self.denominatorOri.split()]  # 分母系数
        sys = ctrl.TransferFunction(numerator, denominator)

        # 设置频率范围
        omega = np.logspace(-2, 2, 1000)  # 从0.01到100，共1000个点

        # 获取Bode图数据
        mag, phase, _ = ctrl.bode(sys, omega, dB=True, Hz=True, deg=True, plot=False)

        # 创建一个图形和两个子图
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

        # 绘制幅频图
        ax1.semilogx(omega, 20 * np.log10(mag))  # 使用对数坐标绘制频率
        ax1.set_xlabel('Frequency (Hz)')
        ax1.set_ylabel('Magnitude (dB)')
        ax1.set_title('Bode Plot - Magnitude')

        # 绘制相频图
        ax2.semilogx(omega, np.degrees(phase))  # 使用对数坐标绘制频率
        ax2.set_xlabel('Frequency (Hz)')
        ax2.set_ylabel('Phase (degrees)')
        ax2.set_title('Bode Plot - Phase')

        # 调整子图间距
        plt.tight_layout()
        plt.show()

        # 绘制Nyquist图
        plt.figure()
        ctrl.nyquist_plot(sys)
        # plt.plot(-1, 0, 'ro')  # 标记临界点(-1, 0)
        plt.xlabel('Real Part')
        plt.ylabel('Imaginary Part')
        plt.title('Nyquist Plot')
        # plt.legend()
        plt.show()
        # # 绘制Nyquist图
        # plt.figure()
        # # 获取Nyquist图数据
        # real, imag, _ = ctrl.nyquist(sys, omega)
        # # 绘制Nyquist图
        # plt.plot(real, imag, label='Nyquist Plot')

        # 计算幅值裕度和相角裕度
        gm, pm, wcg, wcp = ctrl.margin(sys)
        print("幅值裕度：", round(gm, 2), "dB")
        print("相角裕度：", round(pm, 4), "度")
        print("幅值交叉频率频率：", round(wcg, 4), "rad/s")
        print("相角原始截止频率：", round(wcp, 4), "rad/s")
