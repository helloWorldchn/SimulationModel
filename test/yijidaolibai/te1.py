import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 倒立摆参数
m = 0.1  # 摆杆质量
M = 1.0  # 小车质量
l = 0.5  # 摆杆长度
g = 9.81  # 重力加速度

# PID控制器参数
Kp = 10.0
Ki = 1.0
Kd = 5.0

# 时间参数
dt = 0.01  # 时间步长
t_max = 10.0  # 总时间

# 初始化状态变量
theta = np.pi / 2  # 初始摆角
omega = 0.0  # 初始角速度
x = 0.0  # 初始小车位置
v = 0.0  # 初始小车速度

# 初始化PID控制器变量
integral = 0.0
prev_error = 0.0

# 初始化记录数据的列表
times = []
x_positions = []
velocities = []
angles = []
angular_velocities = []

# 创建动画图形
fig, ax = plt.subplots()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.grid(True)
cart, = ax.plot([], [], 'bo-', lw=2)  # 小车
pole, = ax.plot([], [], 'r-', lw=2)  # 摆杆
angle_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)  # 摆角文本

def update(frame):
    global theta, omega, x, v, integral, prev_error

    # 计算PID控制器输出
    error = theta - np.pi / 2
    integral += error * dt
    derivative = (error - prev_error) / dt
    output = Kp * error + Ki * integral + Kd * derivative
    prev_error = error

    # 计算小车和摆杆的运动
    F = output  # 控制力
    a = (F - m * l * omega**2 * np.sin(theta)) / (M + m)
    alpha = (g * np.sin(theta) + a * np.cos(theta)) / l
    v += a * dt
    x += v * dt
    omega += alpha * dt
    theta += omega * dt

    # 更新图形
    cart.set_data([x - 0.1, x + 0.1], [0, 0])
    pole.set_data([x, x + l * np.sin(theta)], [0, -l * np.cos(theta)])
    angle_text.set_text(f'Angle: {np.degrees(theta):.2f}°')

    # 记录数据
    times.append(frame * dt)
    x_positions.append(x)
    velocities.append(v)
    angles.append(np.degrees(theta))
    angular_velocities.append(np.degrees(omega))

    return cart, pole, angle_text

# 创建动画
ani = animation.FuncAnimation(fig, update, frames=int(t_max / dt), interval=dt * 1000, blit=True)

plt.show()

# 绘制数据曲线图
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.plot(times, x_positions)
plt.title('小车位移')
plt.xlabel('时间(s)')
plt.ylabel('位移(m)')

plt.subplot(2, 2, 2)
plt.plot(times, velocities)
plt.title('小车速度')
plt.xlabel('时间(s)')
plt.ylabel('速度(m/s)')

plt.subplot(2, 2, 3)
plt.plot(times, angles)
plt.title('摆角')
plt.xlabel('时间(s)')
plt.ylabel('角度(°)')

plt.subplot(2, 2, 4)
plt.plot(times, angular_velocities)
plt.title('摆角角速度')
plt.xlabel('时间(s)')
plt.ylabel('角速度(°/s)')

plt.tight_layout()
plt.show()