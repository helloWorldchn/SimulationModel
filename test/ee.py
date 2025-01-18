import numpy as np
import matplotlib.pyplot as plt
import control as ctl

# 系统参数
C = 100.0  # 房间的热容 (J/K)
R = 0.01   # 墙壁的热阻 (K/W)
Q_heater = 1000.0  # 加热器的功率 (W)

# 构建传递函数
num = [1 / (C * R)]
den = [1, 1 / (C * R)]
sys = ctl.tf(num, den)

# PID控制器参数
Kp = 1.0  # 比例增益
Ki = 0.1  # 积分增益
Kd = 0.01  # 微分增益

# 构建PID控制器
pid = ctl.tf([Kd, Kp, Ki], [1, 0])

# 闭环系统
closed_loop_sys = ctl.feedback(pid * sys, 1)

# 阶跃响应仿真
t, y = ctl.step_response(closed_loop_sys, T=np.linspace(0, 100, 1000))

# 绘制响应曲线
plt.plot(t, y)
plt.xlabel('Time (s)')
plt.ylabel('Temperature (K)')
plt.title('Step Response of Room Temperature Control System')
plt.grid()
plt.show()