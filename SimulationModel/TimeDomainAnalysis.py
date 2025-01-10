import math

import control as ctrl
import matplotlib.pyplot as plt
import numpy as np


class TimeDomainAnalysis:

    def __init__(self, numeratorOri="25", denominatorOri="1 6 25") -> None:
        """
        1 时域仿真设计 单位阶跃响应 单位斜坡响应
        :param numeratorOri: 分子字符串
        :param denominatorOri: 分母字符串
        """
        self.numeratorOri = numeratorOri  # 分子字符串
        self.denominatorOri = denominatorOri  # 分母字符串

    def timeDomainAnalysis(self):
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False
        # 创建传递函数，例如 G(s) = 1 / (s^2 + 3s + 2)
        # numerator = [self.c]
        # denominator = [self.a, self.b, self.c]
        numerator = [float(num) for num in self.numeratorOri.split()]
        denominator = [float(num) for num in self.denominatorOri.split()]
        sys = ctrl.TransferFunction(numerator, denominator)

        # 计算单位阶跃响应
        t_step, y_step = ctrl.step_response(sys, T=np.linspace(0, 10, 500))

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
        tolerance = 0.01 * final_value
        settling_time_index = np.where(np.abs(y_step - final_value) <= tolerance)[0]
        # 确保响应在±2%范围内保持稳定
        if len(settling_time_index) > 0:
            for idx in settling_time_index:
                if np.all(np.abs(y_step[idx:] - final_value) <= tolerance):
                    settling_time = t_step[idx]
                    break
            else:
                settling_time = np.nan
        else:
            settling_time = np.nan

        # 打印结果
        print(f"上升时间: {rise_time:.5f} 秒" if not np.isnan(rise_time) else "上升时间: 未找到")
        print(f"峰值时间: {peak_time:.5f} 秒")
        print(f"超调量: {overshoot:.5f}%")
        print(f"调节时间（±2%范围内）: {settling_time:.5f} 秒" if not np.isnan(settling_time) else "调节时间: 未找到")

        # 计算单位斜坡响应
        # 由于control库没有ramp_response函数，我们可以使用forced_response函数
        # 单位斜坡信号可以表示为斜率为1的线性函数，即r(t) = t
        # 我们可以使用scipy.signal中的单位斜坡信号来模拟
        t_ramp = np.linspace(0, 10, 500)
        r_ramp = t_ramp  # 单位斜坡信号
        t_ramp, y_ramp = ctrl.forced_response(sys, t_ramp, r_ramp)

        last_two_elements = denominator[-2:]
        linearFunctionCoefficient, constantCoefficient = last_two_elements
        naturalFrequency = math.sqrt(constantCoefficient)  # 计算自然振荡频率
        dampingRatio = linearFunctionCoefficient / 2 / naturalFrequency  # 计算阻尼比

        print(f"阻尼比: {dampingRatio:.2f}")
        print(f"自然振荡频率: {naturalFrequency:.2f}")

        # 绘制单位阶跃响应和单位斜坡响应
        plt.figure()

        plt.plot(t_step, y_step)
        plt.xlabel('时间')
        plt.ylabel('响应')
        plt.title('单位阶跃响应')
        # plt.grid(True)
        plt.savefig('pic/TimeDomain/step_response.png')
        plt.show()

        plt.plot(t_ramp, y_ramp)
        plt.xlabel('时间')
        plt.ylabel('响应')
        plt.title('单位斜坡响应')
        # plt.grid(True)
        plt.savefig('pic/TimeDomain/ramp_response.png')
        plt.show()

        return rise_time, peak_time, overshoot, settling_time, dampingRatio, naturalFrequency
