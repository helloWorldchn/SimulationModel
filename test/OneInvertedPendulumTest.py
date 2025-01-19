import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
# 定义参数
mass_car = 1.5  # 小车质量
mess_pole = 0.25  # 摆杆质量
l_pendulum_mass = 0.24  # 摆杆转动轴到质心的距离l
inertia_moment = (mess_pole * l_pendulum_mass * l_pendulum_mass) / 3  # 摆杆转动惯量I
f = 0.1  # 摩擦系数
g = 9.81  # 重力加速度

# 计算q
q = (mass_car + mess_pole) * (inertia_moment + mess_pole * l_pendulum_mass ** 2) - (mess_pole * l_pendulum_mass) ** 2


# 定义倒立摆的动力学方程
def pendulum_equations(y, t, Kp, Ki, Kd, u):
    theta, d_theta, x, d_x = y
    e = theta  # 误差
    de = d_theta  # 误差的导数
    ie = e * t  # 误差的积分（近似）
    u_pid = -Kp * e - Ki * ie - Kd * de + u  # PID控制律

    d2_theta = (mess_pole * l_pendulum_mass * g * np.sin(theta) - f * d_x * np.cos(theta) + u_pid) / (
                4 / 3 * mess_pole * l_pendulum_mass ** 2 - mess_pole * l_pendulum_mass ** 2 * np.cos(theta) ** 2 / (
                    mass_car + mess_pole))
    d2_x = (mess_pole * l_pendulum_mass * d_theta ** 2 * np.sin(theta) + mess_pole * g * np.sin(theta) * np.cos(
        theta) - u_pid * np.cos(theta)) / (mass_car + mess_pole - mess_pole * np.cos(theta) ** 2)

    return [d_theta, d2_theta, d_x, d2_x]


# PID控制器参数
Kp = 100
Ki = 10
Kd = 10

# 初始状态
y0 = [np.pi / 6, 0, 0, 0]  # 初始角度为30度，初始角速度、小车位置和速度均为0

# 时间
t_max = 60.0  # 仿真时间（秒）
dt = 0.01  # 时间步长（秒）
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
plt.show()
