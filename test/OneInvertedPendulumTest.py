import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
# 定义参数
M = 1.0  # 小车质量（kg）
m = 0.1  # 摆杆质量（kg）
l = 0.5  # 摆杆转动轴到质心的距离（m）
I = 0.01  # 摆杆的转动惯量（kg·m²）
f = 0.1  # 摩擦系数
g = 9.81  # 重力加速度（m/s²）

# 时间参数
t_start = 0  # 开始时间
t_end = 100  # 结束时间
dt = 0.01  # 时间步长
t = np.arange(t_start, t_end, dt)

# 初始状态
theta_0 = np.pi / 6  # 初始摆角（弧度）
omega_0 = 0  # 初始摆杆角速度（rad/s）
x_0 = 0  # 初始小车位移（m）
v_0 = 0  # 初始小车速度（m/s）

# PID 控制器参数
Kp = 40  # 比例系数
Ki = 1.5   # 积分系数
Kd = 7   # 微分系数

# 初始化状态变量
theta = theta_0
omega = omega_0
x = x_0
v = v_0

# 初始化误差和积分项
error = 0
integral = 0
previous_error = 0

# 初始化存储结果的列表
theta_list = []
omega_list = []
x_list = []
v_list = []

# 模拟过程
for i in range(len(t)):
    # 计算当前误差
    error = theta - np.pi / 2  # 以摆杆竖直向上为平衡点

    # 计算积分项
    integral += error * dt

    # 计算微分项
    derivative = (error - previous_error) / dt

    # 计算控制力
    F = Kp * error + Ki * integral + Kd * derivative

    # 更新状态变量
    theta_ddot = (g * np.sin(theta) * np.cos(theta) - l * omega ** 2 * np.sin(2 * theta) / 2 - F * np.cos(theta) / (M + m) - f * v * np.cos(theta) / (M + m)) / (l * (4 / 3 - m * np.cos(theta) ** 2 / (M + m)))
    x_ddot = (F + m * l * theta_ddot * np.cos(theta) - m * l * omega ** 2 * np.sin(theta) - f * v) / (M + m)

    omega += theta_ddot * dt
    theta += omega * dt
    v += x_ddot * dt
    x += v * dt

    # 存储结果
    theta_list.append(theta)
    omega_list.append(omega)
    x_list.append(x)
    v_list.append(v)

    # 更新前一个误差
    previous_error = error

# 输出最终状态
print(f"最终摆角 (θ): {theta:.6f} rad")
print(f"最终摆杆角速度 (ω): {omega:.6f} rad/s")
print(f"最终小车位移 (x): {x:.6f} m")
print(f"最终小车速度 (v): {v:.6f} m/s")

# 绘图
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.plot(t, theta_list)
plt.title('摆角大小')
plt.xlabel('时间 (s)')
plt.ylabel('摆角 (rad)')

plt.subplot(2, 2, 2)
plt.plot(t, omega_list)
plt.title('摆杆角速度')
plt.xlabel('时间 (s)')
plt.ylabel('角速度 (rad/s)')

plt.subplot(2, 2, 3)
plt.plot(t, v_list)
plt.title('小车速度')
plt.xlabel('时间 (s)')
plt.ylabel('速度 (m/s)')

plt.subplot(2, 2, 4)
plt.plot(t, x_list)
plt.title('小车位移')
plt.xlabel('时间 (s)')
plt.ylabel('位移 (m)')

plt.tight_layout()
plt.show()