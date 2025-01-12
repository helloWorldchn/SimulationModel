import numpy as np  # 导入numpy库
import matplotlib.pyplot as plt  # 导入matplotlib库

plt.rcParams["font.sans-serif"] = ["SimHei"]

g = 9.81
t_min = 0
t_max = 100
step = 1

# 创建时间数组
t = np.arange(t_min, t_max, step)  # 从0到t_max以dt为步长生成时间数组

# 计算落体高度
h = 0.5 * float(g) * t ** 2  # 使用自由落体公式计算高度

# 可视化结果
plt.plot(t, h)
plt.title("自由落体仿真")
plt.xlabel("时间 (s)")
plt.ylabel("高度 (m)")
plt.grid(True)  # 显示网格
plt.savefig("pic/FreeFall/freeFall.png")
plt.show()  # 显示图形
