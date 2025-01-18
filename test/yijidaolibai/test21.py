import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 倒立摆参数
M = 5.0  # 小车质量（kg）
m = 1.0  # 摆杆质量（kg）
l = 1.0  # 摆杆长度（m）
g = 9.81  # 重力加速度（m/s²）

# 摩擦力参数
mu_x = 0.1  # 小车摩擦力系数
mu_theta = 0.05  # 摆杆摩擦力系数

# PID控制器参数
Kp = 15.0  # 比例系数
Ki = 2.0   # 积分系数
Kd = 3.0   # 微分系数

# 系统状态变量：[x, dx/dt, theta, dtheta/dt]
# x：小车位置
# dx/dt：小车速度
# theta：摆杆与竖直方向的夹角
# dtheta/dt：摆杆角速度

def pid_controller(error, prev_error, integral):
    integral += error
    integral = np.clip(integral, -10, 10)  # 限幅积分项
    derivative = error - prev_error
    output = Kp * error + Ki * integral + Kd * derivative
    return output, integral

def inverted_pendulum(state, t, u):
    x, dx, theta, dtheta = state
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    # 计算摩擦力
    friction_x = -mu_x * np.sign(dx)  # 小车摩擦力
    friction_theta = -mu_theta * np.sign(dtheta)  # 摆杆摩擦力

    # 计算系统动力学方程
    ddx = (u + m * l * dtheta ** 2 * sin_theta - m * g * sin_theta * cos_theta + friction_x) / (M + m * sin_theta ** 2)
    ddtheta = (g * sin_theta - cos_theta * ddx + friction_theta) / l

    return [dx, ddx, dtheta, ddtheta]

# 初始状态
initial_state = [0, 0, np.pi / 4, 0]  # 初始小车位置为0，速度为0，摆杆初始角度为45度，角速度为0

# 时间参数
t_span = (0, 10)  # 仿真时间范围：0到10秒
t = np.linspace(*t_span, 1000)  # 时间点

# 仿真
state = initial_state
integral = 0
prev_error = 0
states = [state]

for i in range(len(t) - 1):
    # 计算控制输入
    target_theta = 0  # 目标角度为0
    error = state[2] - target_theta  # 以摆杆角度与目标角度的差值作为误差
    u, integral = pid_controller(error, prev_error, integral)
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
plt.plot(t, states[:, 3], label='摆杆角速度')
plt.legend()
plt.xlabel('时间（s）')
plt.ylabel('摆杆状态')

plt.tight_layout()
plt.show()