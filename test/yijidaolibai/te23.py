import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
# 定义参数
M = 1.5  # 小车质量
m = 0.25  # 摆杆质量
l = 0.24  # 摆杆转动轴到质心的距离
I = 0.048  # 摆杆质量
f = 0.1  # 摩擦系数
g = 9.81  # 重力加速度

# 计算q
q = (M + m) * (I + m * l**2) - (m * l)**2

# 定义倒立摆的动力学方程
def pendulum_equations(y, t, Kp, Ki, Kd, u):
    theta, d_theta, x, d_x = y
    e = theta  # 误差
    de = d_theta  # 误差的导数
    ie = e * t  # 误差的积分（近似）
    u_pid = -Kp * e - Ki * ie - Kd * de + u  # PID控制律

    d2_theta = (m * l * g * np.sin(theta) - f * d_x * np.cos(theta) + u_pid) / (4/3 * m * l**2 - m * l**2 * np.cos(theta)**2 / (M + m))
    d2_x = (m * l * d_theta**2 * np.sin(theta) + m * g * np.sin(theta) * np.cos(theta) - u_pid * np.cos(theta)) / (M + m - m * np.cos(theta)**2)

    return [d_theta, d2_theta, d_x, d2_x]

# PID控制器参数
Kp = 100
Ki = 10
Kd = 10

# 初始状态
y0 = [np.pi/6, 0, 0, 0]  # 初始角度为30度，初始角速度、小车位置和速度均为0

# 时间
t = np.linspace(0, 2, 200)  # 仿真时间为10秒

# 求解微分方程
u = 0  # 控制输入
solution = odeint(pendulum_equations, y0, t, args=(Kp, Ki, Kd, u))

# 绘制结果
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(t, solution[:, 0])
plt.title('倒立摆角度')
plt.xlabel('时间(s)')
plt.ylabel('角度(rad)')

plt.subplot(2, 1, 2)
plt.plot(t, solution[:, 2])
plt.title('小车位置')
plt.xlabel('时间(s)')
plt.ylabel('位置(m)')

plt.tight_layout()
plt.show()