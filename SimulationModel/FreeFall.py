import numpy as np  # 导入numpy库
import matplotlib.pyplot as plt  # 导入matplotlib库


class FreeFall:
    plt.rcParams["font.sans-serif"] = ["SimHei"]

    def __init__(self, g=9.81, t_max=10, dt=0.1) -> None:
        self.g = g  # 重力加速度 (m/s^2)
        self.t_max = t_max  # 最大时间 (s)
        self.dt = dt  # 时间步长 (s)

    def freeFall(self):
        # 创建时间数组
        t = np.arange(0, float(self.t_max), float(self.dt))  # 从0到t_max以dt为步长生成时间数组

        # 计算落体高度
        h = 0.5 * float(self.g) * t ** 2  # 使用自由落体公式计算高度

        # 可视化结果
        plt.plot(t, h)
        plt.title("自由落体仿真")
        plt.xlabel("时间 (s)")
        plt.ylabel("高度 (m)")
        plt.grid(True)  # 显示网格
        plt.savefig("pic/FreeFall/freeFall.png")
        plt.show()  # 显示图形
