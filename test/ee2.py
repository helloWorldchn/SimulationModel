import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from control import lqr, ss

# 定义倒立摆的参数
L = 1.0  # 摆杆长度
m_cart = 1.0  # 小车质量
m_pend = 0.1  # 摆杆质量
g = 9.81  # 重力加速度

# 状态空间模型参数
A = np.array([
    [0, 1, 0, 0],
    [0, -(m_pend + m_cart) * g / (L * (m_pend + m_cart)), (m_pend + m_cart) / (m_pend * L), 0],
    [0, 0, 0, 1],
    [0, (m_pend + m_cart) * g / (L * (m_pend + m_cart)), -(1 / L), 0]
])

B = np.array([
    [0],
    [1 / (m_pend + m_cart)],
    [0],
    [-1 / (m_pend * L)]
])

C = np.array([
    [1, 0, 0, 0],
    [0, 0, 1, 0]
])

D = np.zeros((2, 1))

# 创建状态空间系统
sys = ss(A, B, C, D)

# 设计LQR控制器
Q = np.eye(4)  # 状态权重矩阵
R = np.array([[1]])  # 控制输入权重矩阵
K, S, e = lqr(A, B, Q, R)

# 定义仿真函数
def inverted_pendulum_simulation(initial_state, t_span):
    def dynamics(t, state):
        x, x_dot, theta, theta_dot = state
        u = -K @ np.array([x, x_dot, theta, theta_dot])  # 应用LQR控制器
        dxdt = np.array([
            x_dot,
            (m_pend * L * theta_dot**2 * np.sin(theta) + m_pend * g * np.sin(theta) * np.cos(theta) + u) / (m_cart + m_pend),
            theta_dot,
            ((m_cart + m_pend) * g * np.sin(theta) - u * np.cos(theta) - m_pend * L * theta_dot**2 * np.sin(theta) * np.cos(theta)) / (L * (m_pend + m_cart - m_pend * np.cos(theta)**2))
        ])
        return dxdt

    sol = solve_ivp(dynamics, t_span, initial_state, t_eval=np.linspace(t_span[0], t_span[1], 1000))
    return sol

# 初始状态 [x, x_dot, theta, theta_dot]
initial_state = np.array([0, 0, np.pi / 2, 0])  # 初始时摆杆竖直向下，小车静止
t_span = (0, 10)  # 仿真时间

# 运行仿真
sol = inverted_pendulum_simulation(initial_state, t_span)

# 绘制结果
plt.figure()
plt.subplot(2, 1, 1)
plt.plot(sol.t, sol.y[0], label='x (position)')
plt.plot(sol.t, sol.y[2], label='theta (angle)')
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel('Position and Angle')

plt.subplot(2, 1, 2)
plt.plot(sol.t, sol.y[1], label='x_dot (velocity)')
plt.plot(sol.t, sol.y[3], label='theta_dot (angular velocity)')
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel('Velocity and Angular Velocity')

plt.tight_layout()
plt.show()