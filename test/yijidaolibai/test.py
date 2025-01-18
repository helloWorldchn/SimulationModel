import numpy as np
import matplotlib.pyplot as plt
from control import TransferFunction, feedback, step_response

# 定义参数
M = 1.5  # 小车质量
m = 0.25  # 摆杆质量
l = 0.24  # 摆杆转动轴到质心的距离
I = 0.048  # 摆杆转动惯量
f = 0.1  # 摩擦系数
g = 9.81  # 重力加速度

# 计算 q
q = (M + m) * (I + m * l**2) - (m * l)**2

# 定义传递函数的分子和分母
numerator = [m * l / q, 0, 0]
denominator = [1, f * (I + m * l**2) / q, -(M + m) * m * g * l / q, 0, -f * m * g * l]

# 创建传递函数
sys = TransferFunction(numerator, denominator)

# 定义补偿器参数
P = 100
I = 1
D = 15
N = 100

# 创建补偿器传递函数
comp_numerator = [D * N, P * N + I, P]
comp_denominator = [N, 1]
comp = TransferFunction(comp_numerator, comp_denominator)

# 串联补偿器和系统
open_loop = sys * comp

# 计算闭环传递函数
closed_loop = feedback(open_loop, 1)

# 计算阶跃响应
T, yout = step_response(closed_loop)

# 绘制阶跃响应
plt.figure()
plt.plot(T, yout)
plt.title('Step Response of the Closed-Loop System')
plt.xlabel('Time (s)')
plt.ylabel('Output')
plt.grid(True)
plt.show()