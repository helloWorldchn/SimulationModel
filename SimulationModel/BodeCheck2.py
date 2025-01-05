import control as ctrl
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 定义传递函数
num = [100]  # 分子系数
den = [0.001, 0.11, 1, 0]  # 分母系数
sys = ctrl.TransferFunction(num, den)

# 设置频率范围
omega = np.logspace(-1, 4, 1000)  # 从0.01到100，共1000个点

# 获取Bode图数据
mag, phase, _ = ctrl.bode(sys, omega, dB=True, Hz=False, deg=True, plot=False)

# 创建一个图形和两个子图
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# 绘制幅频图
ax1.semilogx(omega, 20 * np.log10(mag))  # 使用对数坐标绘制频率
ax1.set_xlabel('Frequency (rad/s)')
ax1.set_ylabel('Magnitude (dB)')
ax1.set_title('Bode Plot - Magnitude (Original System)')

# 绘制相频图
ax2.semilogx(omega, phase)  # 使用对数坐标绘制频率
ax2.set_xlabel('Frequency (rad/s)')
ax2.set_ylabel('Phase (degrees)')
ax2.set_title('Bode Plot - Phase (Original System)')

# 调整子图间距
plt.tight_layout()
plt.show()

# 计算原始系统的幅值裕度和相角裕度
gm, pm, wg, wp = ctrl.margin(sys)
print("原始系统幅值裕度：", round(gm, 2), "dB")
print("原始系统相角裕度：", round(pm, 4), "度")
print("原始系统幅值交叉频率：", round(wg, 4), "rad/s")
print("原始系统相角交叉频率：", round(wp, 4), "rad/s")

# 设置目标相角裕度
desired_pm = 20  # 目标相角裕度
phase_margin_needed = desired_pm - pm

# 设计超前校正器
# 计算超前校正器的参数
alpha_lead = (180 + desired_pm) / (180 + pm)
T_lead = 1 / (wp * np.sqrt(alpha_lead))
num_lead = [T_lead, 1]
den_lead = [alpha_lead * T_lead, 1]
lead_compensator = ctrl.TransferFunction(num_lead, den_lead)
sys_lead = sys * lead_compensator

# 获取超前校正后的Bode图数据
mag_lead, phase_lead, _ = ctrl.bode(sys_lead, omega, dB=True, Hz=False, deg=True, plot=False)

# 创建一个新的图形和两个子图（超前校正）
fig_lead, (ax1_lead, ax2_lead) = plt.subplots(2, 1, figsize=(10, 8))

# 绘制超前校正后的幅频图
ax1_lead.semilogx(omega, 20 * np.log10(mag_lead))  # 使用对数坐标绘制频率
ax1_lead.set_xlabel('Frequency (rad/s)')
ax1_lead.set_ylabel('Magnitude (dB)')
ax1_lead.set_title('Bode Plot - Magnitude (Lead Compensated System)')

# 绘制超前校正后的相频图
ax2_lead.semilogx(omega, phase_lead)  # 使用对数坐标绘制频率
ax2_lead.set_xlabel('Frequency (rad/s)')
ax2_lead.set_ylabel('Phase (degrees)')
ax2_lead.set_title('Bode Plot - Phase (Lead Compensated System)')

# 调整子图间距
plt.tight_layout()
plt.show()

# 计算超前校正后的幅值裕度和相角裕度
gm_lead, pm_lead, wg_lead, wp_lead = ctrl.margin(sys_lead)
print("超前校正后幅值裕度：", round(gm_lead, 2), "dB")
print("超前校正后相角裕度：", round(pm_lead, 4), "度")
print("超前校正后幅值交叉频率：", round(wg_lead, 4), "rad/s")
print("超前校正后相角交叉频率：", round(wp_lead, 4), "rad/s")
print("超前校正装置分子：", num_lead)
print("超前校正装置分母：", den_lead)

# 设计滞后校正器
# 计算滞后校正器的参数
alpha_lag = (180 + pm) / (180 + desired_pm)
T_lag = 1 / (wg * np.sqrt(alpha_lag))
num_lag = [alpha_lag * T_lag, 1]
den_lag = [T_lag, 1]
lag_compensator = ctrl.TransferFunction(num_lag, den_lag)
sys_lag = sys * lag_compensator

# 获取滞后校正后的Bode图数据
mag_lag, phase_lag, _ = ctrl.bode(sys_lag, omega, dB=True, Hz=False, deg=True, plot=False)

# 创建一个新的图形和两个子图（滞后校正）
fig_lag, (ax1_lag, ax2_lag) = plt.subplots(2, 1, figsize=(10, 8))

# 绘制滞后校正后的幅频图
ax1_lag.semilogx(omega, 20 * np.log10(mag_lag))  # 使用对数坐标绘制频率
ax1_lag.set_xlabel('Frequency (rad/s)')
ax1_lag.set_ylabel('Magnitude (dB)')
ax1_lag.set_title('Bode Plot - Magnitude (Lag Compensated System)')

# 绘制滞后校正后的相频图
ax2_lag.semilogx(omega, phase_lag)  # 使用对数坐标绘制频率
ax2_lag.set_xlabel('Frequency (rad/s)')
ax2_lag.set_ylabel('Phase (degrees)')
ax2_lag.set_title('Bode Plot - Phase (Lag Compensated System)')

# 调整子图间距
plt.tight_layout()
plt.show()

# 计算滞后校正后的幅值裕度和相角裕度
gm_lag, pm_lag, wg_lag, wp_lag = ctrl.margin(sys_lag)
print("滞后校正后幅值裕度：", round(gm_lag, 2), "dB")
print("滞后校正后相角裕度：", round(pm_lag, 4), "度")
print("滞后校正后幅值交叉频率：", round(wg_lag, 4), "rad/s")
print("滞后校正后相角交叉频率：", round(wp_lag, 4), "rad/s")
print("滞后校正装置分子：", num_lag)
print("滞后校正装置分母：", den_lag)
