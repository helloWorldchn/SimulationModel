import tkinter as tk
from tkinter import Toplevel
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from TimeDomainAnalysis import TimeDomainAnalysis


# 定义四个不同的方法
def test1(input1, input2):
    # "25"  "1 6 25"
    rise_time, peak_time, overshoot, settling_time, dampingRatio, naturalFrequency,t_step, y_step,t_ramp, y_ramp = TimeDomainAnalysis(input1, input2).timeDomainAnalysis()

    output1 = f"上升时间: {rise_time:.5f} 秒" if not np.isnan(rise_time) else "上升时间: 未找到"
    output2 = f"峰值时间: {peak_time:.5f} 秒"
    output3 = f"超调量: {overshoot:.5f} %"
    output4 = f"调节时间（±2%范围内）: {settling_time:.5f} 秒" if not np.any(settling_time) else "调节时间: 未找到"
    output5 = f"阻尼比: {dampingRatio:.2f}"
    output6 = f"自然振荡频率: {naturalFrequency:.2f}"
    return output1, output2, output3, output4, output5, output6, t_step, y_step,t_ramp, y_ramp

def test2(input1, input2, input3):
    output1 = f"test2输出1: {input1} + {input2} + {input3}"
    output2 = f"test2输出2: {input1} * {input2} * {input3}"
    output3 = f"test2输出3: {input1} - {input2} - {input3}"
    return output1, output2, output3

def test3(input1, input2):
    output1 = f"test3输出1: {input1} * 2"
    output2 = f"test3输出2: {input2} * 3"
    output3 = f"test3输出3: {input1} + {input2} * 4"
    return output1, output2, output3

def test4(input1, input2):
    output1 = f"test4输出1: {input1} ** 2"
    output2 = f"test4输出2: {input2} ** 3"
    output3 = f"test4输出3: {input1} + {input2} ** 4"
    return output1, output2, output3

# 创建通用界面模板
def create_interface(root, method, title, input_labels, window_size):
    new_window = Toplevel(root)
    new_window.title(title)
    new_window.geometry(window_size)  # 设置窗口大小

    # 创建输入框
    inputs = []
    for label_text in input_labels:
        input_label = tk.Label(new_window, text=label_text)
        input_label.pack()
        input_entry = tk.Entry(new_window)
        input_entry.pack()
        inputs.append(input_entry)

    # 创建输出框
    output1 = tk.Label(new_window, text="")
    output1.pack()
    output2 = tk.Label(new_window, text="")
    output2.pack()
    output3 = tk.Label(new_window, text="")
    output3.pack()
    output4 = tk.Label(new_window, text="")
    output4.pack()
    output5 = tk.Label(new_window, text="")
    output5.pack()
    output6 = tk.Label(new_window, text="")
    output6.pack()

    # 定义按钮点击事件
    def on_button_click():
        # 获取输入值
        input_values = [input_entry.get() for input_entry in inputs]
        # 调用方法并获取输出
        if method == test1:
            out1, out2, out3, out4, out5, out6,t_step, y_step,t_ramp, y_ramp  = method(*input_values)
            # 更新输出框内容
            output1.config(text=out1)
            output2.config(text=out2)
            output3.config(text=out3)
            output4.config(text=out4)
            output5.config(text=out5)
            output6.config(text=out6)
            # 绘制plot图
            # fig, axs = plt.subplots(1, 2, figsize=(10, 5))
            # axs[0].plot(t_step, y_step)
            # axs[1].plot(t_ramp, y_ramp)
            # canvas = FigureCanvasTkAgg(fig, master=new_window)
            # canvas.draw()
            # canvas.get_tk_widget().pack()
            # 绘制第一张plot图
            fig1 = plt.Figure(figsize=(5, 4), dpi=100)
            ax1 = fig1.add_subplot(111)
            ax1.plot(t_step, y_step)
            ax1.set_xlabel('时间')
            ax1.set_ylabel('响应')
            ax1.set_title('单位阶跃响应')
            canvas1 = FigureCanvasTkAgg(fig1, master=new_window)
            canvas1.draw()
            canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # 绘制第二张plot图
            fig2 = plt.Figure(figsize=(5, 4), dpi=100)
            ax2 = fig2.add_subplot(111)
            ax2.plot(t_ramp, y_ramp)
            ax2.set_xlabel('时间')
            ax2.set_ylabel('响应')
            ax1.set_title('单位斜坡响应')
            canvas2 = FigureCanvasTkAgg(fig2, master=new_window)
            canvas2.draw()
            canvas2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        elif method == test2:
            out1, out2, out3 = method(*input_values)
        elif method == test3:
            out1, out2, out3 = method(*input_values)
        elif method == test4:
            out1, out2, out3 = method(*input_values)
        else:
            out1, out2, out3 = method(*input_values[:2])


    # 创建按钮
    button = tk.Button(new_window, text="执行", command=on_button_click)
    button.pack()

# 创建主窗口
root = tk.Tk()
root.title("主界面")
root.geometry("800x600")

# 创建四个选项按钮
buttons = [
    ("时域仿真设计", test1, ["输入分子:", "输入分母:"], "1000x1000", 25),
    ("根轨迹仿真设计", test2, ["输入分子:", "输入分母:", "开环增益:"], "700x450", 25),
    ("频域仿真设计", test3, ["输入分子:", "输入分母:"], "700x450", 25),
    ("选项4", test4, ["输入M:", "输入N:"], "700x450", 25)
]

for title, method, input_labels, window_size, button_width in buttons:
    button = tk.Button(root, text=title, width=button_width, command=lambda method=method, title=title, input_labels=input_labels, window_size=window_size: create_interface(root, method, title, input_labels, window_size))
    button.pack(pady=5)  # 添加垂直间距

# 运行主循环
root.mainloop()