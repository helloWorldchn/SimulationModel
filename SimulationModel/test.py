import control as ctrl
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 定义原始传递函数
num = [10]  # 分子系数
den = [1, 6, 5, 0]  # 分母系数
sys = ctrl.TransferFunction(num, den)

# 设置频率范围
omega = np.logspace(-2, 2, 1000)  # 从0.01到100，共1000个点

# 获取Bode图数据
mag, phase, _ = ctrl.bode(sys, omega, dB=True, Hz=True, deg=True, plot=False)

# 创建一个图形和两个子图
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# 绘制幅频图
ax1.semilogx(omega, 20 * np.log10(mag))  # 使用对数坐标绘制频率
ax1.set_xlabel('Frequency (Hz)')
ax1.set_ylabel('Magnitude (dB)')
ax1.set_title('Bode Plot - Magnitude')

# 绘制相频图
ax2.semilogx(omega, np.degrees(phase))  # 使用对数坐标绘制频率
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Phase (degrees)')
ax2.set_title('Bode Plot - Phase')

# 调整子图间距
plt.tight_layout()
plt.show()

# 计算原始幅值裕度和相角裕度
gm, pm, wg, wp = ctrl.margin(sys)
print("原始幅值裕度：", round(gm, 2), "dB")
print("原始相角裕度：", round(pm, 4), "度")

# 设计相位补偿器
# 假设我们选择零点z和极点p
z = 0.1  # 零点
p = 10   # 极点
C = ctrl.TransferFunction([1, z], [1, p])

# 校正后的传递函数
sys_c = ctrl.series(C, sys)

# 获取校正后的Bode图数据
mag_c, phase_c, _ = ctrl.bode(sys_c, omega, dB=True, Hz=True, deg=True, plot=False)

# 创建一个新的图形和两个子图
fig_c, (ax1_c, ax2_c) = plt.subplots(2, 1, figsize=(10, 8))

# 绘制校正后的幅频图
ax1_c.semilogx(omega, 20 * np.log10(mag_c))  # 使用对数坐标绘制频率
ax1_c.set_xlabel('Frequency (Hz)')
ax1_c.set_ylabel('Magnitude (dB)')
ax1_c.set_title('Bode Plot - Magnitude (Corrected)')

# 绘制校正后的相频图
ax2_c.semilogx(omega, np.degrees(phase_c))  # 使用对数坐标绘制频率
ax2_c.set_xlabel('Frequency (Hz)')
ax2_c.set_ylabel('Phase (degrees)')
ax2_c.set_title('Bode Plot - Phase (Corrected)')

# 调整子图间距
plt.tight_layout()
plt.show()

# 计算校正后的幅值裕度和相角裕度
gm_c, pm_c, wg_c, wp_c = ctrl.margin(sys_c)
print("校正后幅值裕度：", round(gm_c, 2), "dB")
print("校正后相角裕度：", round(pm_c, 4), "度")

# 打印校正装置的分子和分母
print("校正装置分子：", C.num)
print("校正装置分母：", C.den)