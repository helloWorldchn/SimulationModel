import numpy as np
import matplotlib.pyplot as plt


# 定义传递函数，这里使用简单的正弦函数作为例子
def transfer_function(t):
    return np.sin(t)
# 定义传递函数为二阶分子方程

def transfer_function2(t, n, a, b, c):
    numerator = n
    denominator = a * t**2 + b * t + c
    return numerator / denominator


def transfer_function1(t):
    numerator = 25
    denominator = 1 * t**2 + 6 * t + 25
    return numerator / denominator

# 定义单位阶跃响应的模型
def unit_step_response(ts, tf, dt):
    t = np.arange(ts, tf + dt, dt)
    step_response = np.zeros(t.shape)
    for i in range(len(t)):
        if t[i] >= ts:
            step_response[i] = 1
    return t, step_response


# 定义传递函数与单位阶跃响应的乘积
def product_of_transfer_and_step_response(t, step_response, transfer_func):
    return step_response * transfer_func(t)


# 设置时间参数
sampling_time = 0  # 开始采样时间
final_time = 10  # 结束采样时间
dt = 0.01  # 采样间隔

# 获取单位阶跃响应
t, step_response = unit_step_response(sampling_time, final_time, dt)

# 计算传递函数与单位阶跃响应的乘积
product = product_of_transfer_and_step_response(t, step_response, transfer_function1)

# 绘制图形并寻找上升时间和峰值时间
plt.plot(t, product)
plt.title('Unit Step Response x Transfer Function')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid()

# 寻找上升时间和峰值时间
rising_time = np.where(np.diff(np.sign(product - 0.5 * np.max(product))))[0]
peak_times = np.where(product == np.max(product))[0]

# 打印结果
print(f"Rising time: {t[rising_time[0]]}")
print(f"Peak times: {t[peak_times]}")

plt.show()