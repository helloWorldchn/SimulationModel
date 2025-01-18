import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
# 定义参数
M = 1.5  # 小车质量（kg）
m = 0.25  # 摆杆质量（kg）
l = 0.24  # 摆杆转动轴到质心的距离（m）
I = 0.048  # 摆杆的转动惯量（kg·m²）
f = 0.1  # 摩擦系数
g = 9.81  # 重力加速度（m/s²）

# 定义倒立摆的动力学方程
def pendulum_equations(y, t, M, m, l, I, f, g):
    theta, omega = y  # theta为转角，omega为角速度
    # 计算角加速度alpha
    alpha = (m * g * l * np.sin(theta) - f * omega) / (I + m * l**2)
    return [omega, alpha]

# 初始条件
theta0 = np.pi / 4  # 初始转角为45度
omega0 = 0  # 初始角速度为0
y0 = [theta0, omega0]

# 时间范围
t = np.linspace(0, 10, 500)  # 从0到10秒，共500个时间点

# 求解微分方程
solution = odeint(pendulum_equations, y0, t, args=(M, m, l, I, f, g))

# 提取转角数据
theta = solution[:, 0]

# 绘制转角与时间的关系图
plt.figure(figsize=(10, 6))
plt.plot(t, theta, label='转角')
plt.xlabel('时间（s）')
plt.ylabel('转角（rad）')
plt.title('一级倒立摆转角与时间的关系')
plt.legend()
plt.grid(True)
plt.show()