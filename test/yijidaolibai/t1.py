import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# 倒立摆参数
M = 1.5  # 小车质量（kg）
m = 0.25  # 摆杆质量（kg）
l = 0.24  # 摆杆转动轴到质心的距离（m）
I = 0.048  # 摆杆的转动惯量（kg·m²）
f = 0.1  # 摩擦系数
g = 9.81  # 重力加速度（m/s²）

# PID控制器参数
P = 100.0  # 比例系数
I = 1.0    # 积分系数
D = 15.0   # 微分系数
N = 100.0  # 滤波器系数

# 系统状态变量：[x, dx/dt, theta, dtheta/dt]
# x：小车位置
# dx/dt：小车速度
# theta：摆杆与竖直方向的夹角
# dtheta/dt：摆杆角速度

def pid_controller(error, prev_error, integral, d_error, dt):
    integral += error * dt
    d_error = (error - prev_error) / dt
    filtered_d_error = D * N * d_error / (1 + N * dt)
    output = P * error + I * integral + filtered_d_error
    return output, integral, d_error

def inverted_pendulum(state, t, u):
    x, dx, theta, dtheta = state
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    # 计算系统动力学方程
    denominator = I * (M + m) + M * m * l**2
    ddx = (u - f * dx - m * l * dtheta**2 * sin_theta * cos_theta - m * g * l * sin_theta * cos_theta) / denominator
    ddtheta = (g * sin_theta * (I + M * l**2) + dx**2 * l * m * sin_theta * cos_theta - u * l * cos_theta) / denominator

    return [dx, ddx, dtheta, ddtheta]

# 初始状态
initial_state = [0, 0, np.pi / 4, 0]  # 初始小车位置为0，速度为0，摆杆初始角度为45度，角速度为0

# 时间参数
t_span = (0, 10)  # 仿真时间范围：0到10秒
t = np.linspace(*t_span, 1000)  # 时间点
dt = t[1] - t[0]  # 时间步长

# 仿真
state = initial_state
integral = 0
prev_error = 0
d_error = 0
states = [state]

for i in range(len(t) - 1):
    # 计算控制输入
    error = state[2]  # 以摆杆角度作为误差
    u, integral, d_error = pid_controller(error, prev_error, integral, d_error, dt)
    prev_error = error

    # 解微分方程
    new_state = odeint(inverted_pendulum, state, [t[i], t[i+1]], args=(u,))[1]
    states.append(new_state)
    state = new_state

# 绘制结果
states = np.array(states)
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(t, states[:, 0], label='小车位置')
plt.plot(t, states[:, 1], label='小车速度')
plt.legend()
plt.xlabel('时间（s）')
plt.ylabel('小车状态')

plt.subplot(2, 1, 2)
plt.plot(t, states[:, 2], label='摆杆角度')
plt.legend()
plt.xlabel('时间（s）')
plt.ylabel('摆杆状态')

plt.tight_layout()
plt.show()