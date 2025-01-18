import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.signal import lti, step

# 倒立摆参数
M = 1.5  # 小车质量（kg）
m = 0.25  # 摆杆质量（kg）
l = 0.24  # 摆杆转动轴到质心的距离（m）
I = 0.048  # 摆杆的转动惯量（kg·m²）
f = 0.1  # 摩擦系数
g = 9.81  # 重力加速度（m/s²）

# 计算 q
q = (M + m) * (I + m * l**2) - (m * l)**2

# 动力学方程的系数
num = [m * l / q, 0, 0]
den = [1, f * (I + m * l**2) / q, - (M + m) * m * g * l / q, - f * m * g * l / q]

# 创建传递函数
system = lti(num, den)

# 时间参数
t_span = (0, 10)  # 仿真时间范围：0到10秒
t = np.linspace(*t_span, 1000)  # 时间点

# 计算阶跃响应
t, y = step(system, T=t)

# 绘制结果
plt.figure(figsize=(12, 6))
plt.plot(t, y, label='摆杆角度')
plt.legend()
plt.xlabel('时间（s）')
plt.ylabel('摆杆角度（rad）')
plt.show()