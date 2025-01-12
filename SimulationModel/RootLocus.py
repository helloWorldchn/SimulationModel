import control as ctrl
import matplotlib.pyplot as plt
import numpy as np


class RootLocus:
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False

    def __init__(self, numeratorOri="25", denominatorOri="1 6 25", openLoopGain=10) -> None:
        """
        2  根轨迹仿真设计 开环单位阶跃响应 根轨迹
        :param numeratorOri: 分子字符串
        :param denominatorOri: 分母字符串
        :param openLoopGain: 开环增益
        """
        self.numeratorOri = numeratorOri  # 分子字符串
        self.denominatorOri = denominatorOri  # 分母字符串
        self.openLoopGain = openLoopGain  # 开环增益

    def rootLocus(self):
        # 定义传递函数
        # numerator = [1]  # 分子系数
        # denominator = [1, 3, 2, 0]  # 分母系数
        numerator = [float(num) for num in self.numeratorOri.split()]  # 分子系数
        denominator = [float(num) for num in self.denominatorOri.split()]  # 分母系数
        # 定义开环增益
        openLoopGain = float(self.openLoopGain)  # 选择增益

        sys = ctrl.TransferFunction(numerator, denominator)
        # 计算并绘制单位阶跃响应

        sys_k = sys * openLoopGain

        # 绘制根轨迹
        ctrl.root_locus(sys_k)
        # 绘制根轨迹并获取根轨迹的值
        # 绘制根轨迹并获取根轨迹的根的实部和虚部的数组
        rlist, klist = ctrl.rlocus(sys_k)
        # 计算根轨迹的值的数组
        root_locus_values = np.array(rlist)
        # 绘制根轨迹
        plt.plot(root_locus_values.real, root_locus_values.imag, 'b')
        plt.xlabel('实轴')
        plt.ylabel('虚轴')
        plt.title('根轨迹')
        plt.savefig('pic/RootLocus/rootLocus.png')
        plt.show()

        # 计算并绘制单位阶跃响应
        tStepGain, yStepGain = ctrl.step_response(sys_k)
        plt.plot(tStepGain, yStepGain)
        plt.xlabel('时间')
        plt.ylabel('振幅')
        plt.title('开环单位阶跃响应')
        plt.savefig('pic/RootLocus/step_response.png')
        plt.show()


if __name__ == '__main__':
    RootLocus("1", "1 3 2 0", 10).rootLocus()
