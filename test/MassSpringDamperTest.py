import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
# 定义系统参数
m = 1.0  # 质量
c = 1  # 阻尼系数
k = 2.0  # 弹簧常数


# 定义微分方程
def spring_mass_damper(t, y):
    x, v = y
    dxdt = v
    dvdt = -(c / m) * v - (k / m) * x
    return [dxdt, dvdt]


# 初始条件
x0 = 1.0  # 初始位移
v0 = 0.0  # 初始速度

# 时间范围
t_span = (0, 20)
t_eval = np.linspace(t_span[0], t_span[1], 500)

# 求解微分方程
sol = solve_ivp(spring_mass_damper, t_span, [x0, v0], t_eval=t_eval)

# 绘制结果
plt.figure(figsize=(10, 6))
plt.plot(sol.t, sol.y[0], label='位移 (x)')
plt.plot(sol.t, sol.y[1], label='速度 (v)')
plt.xlabel('时间 (s)')
plt.ylabel('物体')
plt.title('弹簧-质量-阻尼系统')
plt.legend()
plt.grid()
plt.show()
