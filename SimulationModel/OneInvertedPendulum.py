import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


class OneInvertedPendulum:
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False

    def __init__(self, mass_car=1.5, mass_pole=0.25, length_pole=0.24, friction_coefficient=0.1,
                 gravity_acceleration=9.81, Kp=100, Ki=10, Kd=10, t_max=60.0, dt=0.01) -> None:
        """
        一级倒立摆模型仿真
        :param mass_car: 小车质量
        :param mass_pole: 摆杆质量
        :param length_pole: 摆杆转动轴到质心的距离l
        :param friction_coefficient: 摩擦系数f
        :param gravity_acceleration: 重力加速度g
        :param Kp: 比例增益
        :param Ki: 积分增益
        :param Kd: 微分增益
        :param t_max: 仿真时间（秒）
        :param dt: 时间步长（秒）
        """
        self.mass_car = float(mass_car)
        self.mass_pole = float(mass_pole)
        self.length_pole = float(length_pole)
        self.friction_coefficient = float(friction_coefficient)
        self.gravity_acceleration = float(gravity_acceleration)
        self.Kp = float(Kp)
        self.Ki = float(Ki)
        self.Kd = float(Kd)
        self.t_max = float(t_max)
        self.dt = float(dt)

    def oneInvertedPendulum(self):
        # 定义参数
        mass_car = self.mass_car  # 小车质量
        mess_pole = self.mass_pole  # 摆杆质量
        l_pendulum_mass = self.length_pole  # 摆杆转动轴到质心的距离l
        friction_coefficient = self.friction_coefficient  # 摩擦系数f
        gravity_acceleration = self.gravity_acceleration  # 重力加速度g
        # PID控制器参数
        Kp = self.Kp
        Ki = self.Ki
        Kd = self.Kd

        inertia_moment = (1 / 3) * mess_pole * l_pendulum_mass ** 2  # 摆杆转动惯量（kg·m²）I

        # 计算q
        q = (mass_car + mess_pole) * (inertia_moment + mess_pole * l_pendulum_mass ** 2) - (
                mess_pole * l_pendulum_mass) ** 2

        # 定义倒立摆的动力学方程
        def pendulum_equations(y, t, Kp, Ki, Kd, u):
            theta, d_theta, x, d_x = y
            e = theta  # 误差
            de = d_theta  # 误差的导数
            ie = e * t  # 误差的积分（近似）
            u_pid = -Kp * e - Ki * ie - Kd * de + u  # PID控制律

            d2_theta = (mess_pole * l_pendulum_mass * gravity_acceleration * np.sin(
                theta) - friction_coefficient * d_x * np.cos(theta) + u_pid) / (
                               4 / 3 * mess_pole * l_pendulum_mass ** 2 - mess_pole * l_pendulum_mass ** 2 * np.cos(
                           theta) ** 2 / (
                                       mass_car + mess_pole))
            d2_x = (mess_pole * l_pendulum_mass * d_theta ** 2 * np.sin(
                theta) + mess_pole * gravity_acceleration * np.sin(
                theta) * np.cos(
                theta) - u_pid * np.cos(theta)) / (mass_car + mess_pole - mess_pole * np.cos(theta) ** 2)

            return [d_theta, d2_theta, d_x, d2_x]

        # 初始状态
        y0 = [np.pi / 6, 0, 0, 0]  # 初始角度为30度，初始角速度、小车位置和速度均为0

        # 定义仿真参数
        t_max = self.t_max  # 仿真时间（秒）
        dt = self.dt  # 时间步长（秒）
        t = np.arange(0, t_max, dt)  # 时间数组

        # 求解微分方程
        u = 0  # 控制输入
        solution = odeint(pendulum_equations, y0, t, args=(Kp, Ki, Kd, u))

        # 绘制结果
        plt.figure(figsize=(12, 6))
        plt.subplot(2, 2, 1)
        plt.plot(t[:200], solution[:200, 0])  # 取前100个数据点，对应前2秒
        plt.title('倒立摆角度')
        plt.xlabel('时间(s)')
        plt.ylabel('角度(rad)')

        plt.subplot(2, 2, 2)
        plt.plot(t[:200], solution[:200, 1])  # 取前100个数据点，对应前2秒
        plt.title('摆角速度')
        plt.xlabel('时间(s)')
        plt.ylabel('角速度(rad/s)')

        plt.subplot(2, 2, 3)
        plt.plot(t, solution[:, 2])
        plt.title('小车位置')
        plt.xlabel('时间(s)')
        plt.ylabel('位置(m)')

        plt.subplot(2, 2, 4)
        plt.plot(t, solution[:, 3])
        plt.title('小车速度')
        plt.xlabel('时间(s)')
        plt.ylabel('速度(m/s)')

        plt.tight_layout()
        plt.savefig("pic/OneInvertedPendulum/invertedPendulum.png")
        plt.show()


if __name__ == '__main__':
    OneInvertedPendulum(1.5, 0.25, 0.24, 0.1, 9.81, 100, 10, 10, 60, 0.01).oneInvertedPendulum()
