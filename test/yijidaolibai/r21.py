import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lti, step

# 电机参数
R = 1.0  # 电枢回路总电阻 (Ω)
L = 0.1  # 电枢回路总电感 (H)
Kt = 0.1  # 电机转矩常数 (Nm/A)
Ke = 0.1  # 电机反电动势常数 (V·s/rad)
J = 0.01  # 电机转动惯量 (kg·m²)
B = 0.01  # 电机粘滞摩擦系数 (Nm·s/rad)

# 反馈系数
alpha = 0.01  # 转速反馈系数
beta = 0.1    # 电流反馈系数

# 调节器参数
KpI_i = 1.0 / (beta * R)  # 电流调节器比例积分增益
tau_i = L / R              # 电流调节器积分时间常数

KpI_s = 1.0 / (alpha * Ke)  # 转速调节器比例积分增益
tau_s = J / B               # 转速调节器积分时间常数

# 电流环传递函数
num_i = [KpI_i * tau_i, KpI_i]
den_i = [L, R + KpI_i * beta * R]
sys_i = lti(num_i, den_i)

# 转速环传递函数
num_s = [KpI_s * tau_s, KpI_s]
den_s = [J * B, B + KpI_s * alpha * Ke * Kt]
sys_s = lti(num_s, den_s)

# 仿真时间设置
t = np.linspace(0, 10, 1000)  # 仿真时间从0到10秒，共1000个点

# 电流环阶跃响应
t_i, y_i = step(sys_i, T=t)

# 转速环阶跃响应
t_s, y_s = step(sys_s, T=t)

# 绘制仿真图
plt.figure(figsize=(12, 6))

# 绘制电流环阶跃响应
plt.subplot(2, 1, 1)
plt.plot(t_i, y_i, label='Current Loop Response')
plt.title('Current Loop Step Response')
plt.xlabel('Time (s)')
plt.ylabel('Current (A)')
plt.legend()
plt.grid(True)

# 绘制转速环阶跃响应
plt.subplot(2, 1, 2)
plt.plot(t_s, y_s, label='Speed Loop Response')
plt.title('Speed Loop Step Response')
plt.xlabel('Time (s)')
plt.ylabel('Speed (rad/s)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()