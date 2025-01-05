import control as ctrl
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


def plot_bode(sys, omega, title):
    mag, phase, _ = ctrl.bode(sys, omega, dB=True, Hz=True, deg=True, plot=False)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # 绘制幅频图
    ax1.semilogx(omega, 20 * np.log10(mag))  # 使用对数坐标绘制频率
    ax1.set_xlabel('Frequency (Hz)')
    ax1.set_ylabel('Magnitude (dB)')
    ax1.set_title(f'Bode Plot - Magnitude - {title}')

    # 绘制相频图
    ax2.semilogx(omega, np.degrees(phase))  # 使用对数坐标绘制频率
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Phase (degrees)')
    ax2.set_title(f'Bode Plot - Phase - {title}')

    # 调整子图间距
    plt.tight_layout()
    plt.show()


# 定义传递函数
num = [100]  # 分子系数
den = [0.001, 0.11, 1, 0]  # 分母系数
sys = ctrl.TransferFunction(num, den)

# 设置频率范围
omega = np.logspace(-1, 4, 1000)  # 从0.01到100，共1000个点

# 绘制原始系统的Bode图
plot_bode(sys, omega, title='Original System')

# 计算原始系统的幅值裕度和相角裕度
gm, pm, wg, wp = ctrl.margin(sys)
print("原始系统幅值裕度：", round(gm, 2), "dB")
print("原始系统相角裕度：", round(pm, 4), "度")
print("原始系统幅值交叉频率：", round(wg, 4), "rad/s")
print("原始系统相角交叉频率：", round(wp, 4), "rad/s")

# 设置目标相角裕度
desired_pm = 20  # 目标相角裕度
phase_margin_needed = desired_pm

# 超前校正
if phase_margin_needed > 0:
    alpha_lead = (1 - np.sin(np.radians(phase_margin_needed))) / (1 + np.sin(np.radians(phase_margin_needed)))
    T_lead = 1 / (wg * np.sqrt(alpha_lead))
    num_lead = [T_lead, 1]
    den_lead = [alpha_lead * T_lead, 1]
    lead_compensator = ctrl.TransferFunction(num_lead, den_lead)
    sys_lead = sys * lead_compensator

    # 绘制超前校正后的Bode图
    plot_bode(sys_lead, omega, title='Lead Compensated System')

    # 计算超前校正后的幅值裕度和相角裕度
    gm_lead, pm_lead, wg_lead, wp_lead = ctrl.margin(sys_lead)
    print("超前校正后幅值裕度：", round(gm_lead, 2), "dB")
    print("超前校正后相角裕度：", round(pm_lead, 4), "度")
    print("超前校正后幅值交叉频率：", round(wg_lead, 4), "rad/s")
    print("超前校正后相角交叉频率：", round(wp_lead, 4), "rad/s")
    print("超前校正装置分子：", num_lead)
    print("超前校正装置分母：", den_lead)
else:
    print("不需要超前校正")

