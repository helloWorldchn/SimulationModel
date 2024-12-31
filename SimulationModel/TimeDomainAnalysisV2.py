import numpy as np
import matplotlib.pyplot as plt
import control
class TimeDomainAnalysisV2:
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    # 定义传递函数的分子和分母
    def __init__(self,g=9.81,t_max = 10,dt = 0.1) -> None:
        self.g = g # 重力加速度 (m/s^2)
        self.t_max = t_max   # 最大时间 (s)
        self.dt = dt  # 时间步长 (s)

    numerator = [25]

    denominator = [1, 6, 25]

    # 创建传递函数对象

    tf = control.TransferFunction(numerator, denominator)

    # 绘制单位阶跃响应

    t_step, y_step = control.step_response(tf)

    # 计算特征时间
    # 最终值（稳态值），对于单位阶跃输入和此传递函数，由于传递函数增益为1，最终值也应为1
    final_value = 1

    # 上升时间（从0到90%最终值的时间）
    threshold_90 = 0.9 * final_value
    rise_time_index = np.argmax(y_step >= threshold_90)
    rise_time = t_step[rise_time_index] if rise_time_index > 0 else np.nan

    # 峰值时间（达到最大值的时间）
    peak_time_index = np.argmax(y_step)
    peak_time = t_step[peak_time_index]
    peak_value = y_step[peak_time_index]

    # 超调量（超过最终值的最大百分比）
    overshoot = ((peak_value - final_value) / final_value) * 100 if peak_value > final_value else 0

    # 调节时间（达到并保持在最终值±2%范围内的时间）
    tolerance = 0.02 * final_value
    settling_time_index = np.where(np.abs(y_step - final_value) <= tolerance)
    if len(settling_time_index) > 0:
        settling_time = t_step[settling_time_index]
    else:
        settling_time = np.nan

    # 打印结果
    print(f"上升时间: {rise_time:.2f} 秒" if not np.isnan(rise_time) else "上升时间: 未找到")
    print(f"峰值时间: {peak_time:.2f} 秒")
    print(f"超调量: {overshoot:.2f}%")
    print(f"调节时间（±2%范围内）: {settling_time:.2f} 秒" if not np.any(settling_time) else "调节时间: 未找到")


    plt.plot(t_step, y_step)

    plt.xlabel('时间')

    plt.ylabel('响应')

    plt.title('单位阶跃响应')

    plt.grid(True)

    plt.show()







