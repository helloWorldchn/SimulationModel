import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


class MassSpringDamper:
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False

    def __init__(self, m=1.0, k=2.0, c=1) -> None:
        """
        弹簧-质量-阻尼系统
        :param m: 质量
        :param k: 弹簧常数
        :param c: 阻尼系数
        """
        # 定义系统参数
        self.m = float(m)  # 质量
        self.k = float(k)  # 弹簧常数
        self.c = float(c)  # 阻尼系数

    def massSpringDamper(self):
        # 定义系统参数
        m = self.m  # 质量
        k = self.k  # 弹簧常数
        c = self.c  # 阻尼系数

        # 定义微分方程
        def spring_mass_damper(t, y):
            x, v = y
            dxdt = v
            dvdt = -(c / m) * v - (k / m) * x
            return [dxdt, dvdt]

        # 初始条件
        x0 = 1.0  # 初始位移
        v0 = 0.0  # 初始速度

        # 时间范围
        t_span = (0, 20)
        t_eval = np.linspace(t_span[0], t_span[1], 500)

        # 求解微分方程
        sol = solve_ivp(spring_mass_damper, t_span, [x0, v0], t_eval=t_eval)

        # 绘制结果
        plt.figure(figsize=(10, 6))
        plt.plot(sol.t, sol.y[0], label='位移 (x)')
        plt.plot(sol.t, sol.y[1], label='速度 (v)')
        plt.xlabel('时间 (s)')
        plt.ylabel('物体')
        plt.title('弹簧-质量-阻尼系统')
        plt.legend()
        plt.grid()
        plt.savefig("pic/MassSpringDamper/massSpringDamper.png")
        plt.show()


if __name__ == '__main__':
    MassSpringDamper(1, 2, 1).massSpringDamper()
