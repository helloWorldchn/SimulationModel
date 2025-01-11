import math

import control as ctrl
import matplotlib.pyplot as plt
import numpy as np
import control as ctrl
import matplotlib.pyplot as plt
import numpy as np
from control import series

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 定义传递函数
num = [100]  # 分子系数
den = [0.001, 0.11, 1, 0]  # 分母系数
sys = ctrl.TransferFunction(num, den)

# 设置频率范围
omega = np.logspace(-1, 4, 1000)  # 从0.1到10000，共1000个点

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
gm, pm, wcg, wcp = ctrl.margin(sys)
print("原始系统幅值裕度：", round(gm, 2), "dB")
print("原始系统相角裕度：", round(pm, 4), "度")  # phase_margin_original
print("原始系统幅值交叉频率：", round(wcg, 4), "rad/s")
print("原始系统相角交叉频率：", round(wcp, 4), "rad/s")

if pm < 5:
    safety_margin = 10  # 如果原始相角裕度很小，增加安全裕度
elif pm < 10:
    safety_margin = 7  # 如果原始相角裕度较小，适当增加安全裕度
else:
    safety_margin = 5  # 默认安全裕度

# 设置目标相角裕度
desired_pm = 20  # 目标相角裕度
phase_margin_needed = desired_pm - pm + safety_margin  # 需要增加的相角

# 根据系统参数变化调整安全裕度
# 设计超前校正器
# 计算超前校正器的参数
alpha_lead = (1 + np.sin(np.radians(phase_margin_needed))) / (1 - np.sin(np.radians(phase_margin_needed)))
# 计算参数 T
omega_c = wcp * 1.2
T_lead = 1 / (omega_c * np.sqrt(alpha_lead))
# 计算超前校正器的传递函数
num_lead = [alpha_lead * T_lead, 1]
den_lead = [T_lead, 1]
lead_compensator = ctrl.TransferFunction(num_lead, den_lead)
sys_lead = series(sys, lead_compensator)

# 计算目标频率 omega_c
# 找到未校正系统在增益为 -20*log10(alpha) dB 处的频率
target_gain_dB = -20 * np.log10(alpha_lead)
gain_crossover_idx = np.argmin(np.abs(mag - 10 ** (target_gain_dB / 20)))
omega_c = omega[gain_crossover_idx]
T_lead1 = 1 / (omega_c * np.sqrt(alpha_lead))
# sys_lead = sys * lead_compensator
# 输出结果
print(f"未校正系统的相角裕度: {pm} 度")
print(f"目标相角裕度: {desired_pm} 度")
print(f"需要的相位校正量: {phase_margin_needed} 度")
print(f"参数 alpha: {alpha_lead}")
print(f"参数 T: {T_lead}")
print(f"超前校正器的传递函数: {sys}")
print(f"校正后的系统传递函数: {sys_lead}")
print(f"校正后的系统传递函数: {lead_compensator}")

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
gm_lead, pm_lead, wcg_lead, wcp_lead = ctrl.margin(sys_lead)
print("超前校正后幅值裕度：", round(gm_lead, 2), "dB")
print("超前校正后相角裕度：", round(pm_lead, 4), "度")
print("超前校正后幅值交叉频率：", round(wcg_lead, 4), "rad/s")
print("超前校正后相角交叉频率：", round(wcp_lead, 4), "rad/s")
print("超前校正装置分子：", num_lead)
print("超前校正装置分母：", den_lead)


# 设计滞后校验器
# 选择一个合适的频率作为校验器的设计频率，通常选择在增益交界频率附近
design_freq = wcp
# 校验器的设计参数
alpha = (1 + np.sin(np.radians(phase_margin_needed))) / (1 - np.sin(np.radians(phase_margin_needed)))
T = 1 / (design_freq * np.sqrt(alpha))

z = 1 / (T * alpha)
p = 1 / T

# 创建滞后校验器的传递函数
lag_comp = ctrl.TransferFunction([1, z], [1, p])

# 校验后的系统
sys_lag = sys * lag_comp

# 获取校验后系统的Bode图数据
mag_lag, phase_lag, _ = ctrl.bode(sys_lag, omega, dB=True, Hz=False, deg=True, plot=False)

# 绘制校验后系统的Bode图
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# 绘制幅频图
ax1.semilogx(omega, 20 * np.log10(mag_lag))
ax1.set_xlabel('Frequency (rad/s)')
ax1.set_ylabel('Magnitude (dB)')
ax1.set_title('Bode Plot - Magnitude (Lag Compensated System)')

# 绘制相频图
ax2.semilogx(omega, phase_lag)
ax2.set_xlabel('Frequency (rad/s)')
ax2.set_ylabel('Phase (degrees)')
ax2.set_title('Bode Plot - Phase (Lag Compensated System)')

# 调整子图间距
plt.tight_layout()
plt.show()

# 计算校验后系统的幅值裕度和相角裕度
gm_lag, pm_lag, wcg_lag, wcp_lag = ctrl.margin(sys_lag)
print("校验后系统幅值裕度：", round(gm_lag, 2), "dB")
print("校验后系统相角裕度：", round(pm_lag, 4), "度")
print("校验后系统幅值交叉频率：", round(wcg_lag, 4), "rad/s")
print("校验后系统相角交叉频率：", round(wcp_lag, 4), "rad/s")


# 绘制校验后系统的Bode图
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# 绘制幅频图
ax1.semilogx(omega, 20 * np.log10(mag), label='Original System')
ax1.semilogx(omega, 20 * np.log10(mag_lead), label='Lead Compensated System')
ax1.semilogx(omega, 20 * np.log10(mag_lag), label='Lag Compensated System')
ax1.set_xlabel('Frequency (rad/s)')
ax1.set_ylabel('Magnitude (dB)')
ax1.set_title('Bode Plot - Magnitude (Compensated System)')
ax1.legend()

# 绘制相频图
ax2.semilogx(omega, phase, label='Original System')
ax2.semilogx(omega, phase_lead, label='Lead Compensated System')
ax2.semilogx(omega, phase_lag, label='Lag Compensated System')
ax2.set_xlabel('Frequency (rad/s)')
ax2.set_ylabel('Phase (degrees)')
ax2.set_title('Bode Plot - Phase (Compensated System)')
ax2.legend()

# 调整子图间距
plt.tight_layout()
plt.show()
