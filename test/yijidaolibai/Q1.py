import numpy as np
import matplotlib.pyplot as plt
import control

# 定义参数
mCart = 0.5  # 小车质量 (kg)
mPend = 0.2  # 摆杆质量 (kg)
b = 0.1      # 摩擦系数
I = 0.018    # 摆杆的转动惯量 (kg·m²)
g = 9.8      # 重力加速度 (m/s²)
L = 0.3      # 摆杆长度 (m)

# 计算 q
q = (mCart + mPend) * (I + mPend * L**2) - (mPend * L)**2

# 定义传递函数
s = control.tf('s')
P_pend = (mPend * L * s) / (q * s**3 + b * (I + mPend * L**2) * s**2 - (mCart + mPend) * mPend * g * L * s - b * mPend * g * L)
P_cart = ((I + mPend * L**2) * s**2 - mPend * g * L) / (q * s**4 + b * (I + mPend * L**2) * s**3 - (mCart + mPend) * mPend * g * L * s**2 - b * mPend * g * L * s)

# 打印传递函数
print("摆的角度传递函数:")
print(P_pend)
print("小车位置传递函数:")
print(P_cart)

# 仿真
t = np.linspace(0, 10, 1000)  # 时间从 0 到 10 秒，1000 个点
u = np.zeros_like(t)  # 控制输入为零
u[500:] = 1  # 在 t=5 秒时施加一个单位阶跃输入

# 仿真摆的角度响应
t_pend, y_pend = control.step_response(P_pend, T=t)

# 仿真小车位置响应
t_cart, y_cart = control.step_response(P_cart, T=t)

# 绘图
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(t_pend, y_pend)
plt.title('摆的角度响应')
plt.xlabel('时间 (s)')
plt.ylabel('摆角 (rad)')

plt.subplot(2, 1, 2)
plt.plot(t_cart, y_cart)
plt.title('小车位置响应')
plt.xlabel('时间 (s)')
plt.ylabel('位移 (m)')

plt.tight_layout()
plt.show()