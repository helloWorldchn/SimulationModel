import tkinter as tk
from tkinter import Toplevel
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk

from RootLocus import RootLocus
from FrequencyDomain import FrequencyDomain
from FreeFall import FreeFall
from TimeDomainAnalysis import TimeDomainAnalysis


# 定义四个不同的方法
def timeDomainSimu(input1, input2):
    # "25"  "1 6 25"
    rise_time, peak_time, overshoot, settling_time, dampingRatio, naturalFrequency = TimeDomainAnalysis(input1, input2).timeDomainAnalysis()

    output1 = f"上升时间: {rise_time:.5f} 秒" if not np.isnan(rise_time) else "上升时间: 未找到"
    output2 = f"峰值时间: {peak_time:.5f} 秒"
    output3 = f"超调量: {overshoot:.5f} %"
    output4 = f"调节时间（±2%范围内）: {settling_time:.5f} 秒" if not np.any(settling_time) else "调节时间: 未找到"
    output5 = f"阻尼比: {dampingRatio:.2f}"
    output6 = f"自然振荡频率: {naturalFrequency:.2f}"
    return output1, output2, output3, output4, output5, output6

def rootLocusSimu(input1, input2, input3):
    # "1", "1 3 2 0", 10
    RootLocus(input1, input2, input3).rootLocus()

def frequencyDomainSimu(input1, input2):
    # "10", "1 6 5 0"
    gm, pm, wcg, wcp = FrequencyDomain(input1, input2).frequencyDomain()
    output1 = f"幅值裕度：", {round(gm, 2)}, "dB"
    output2 = f"相角裕度：", {round(pm, 4)}, "度"
    output3 = f"幅值交叉频率频率：", {round(wcg, 4)}, "rad/s"
    output4 = f"相角原始截止频率：", {round(wcp, 4)}, "rad/s"
    return output1, output2, output3, output4

def checkSimu(input1, input2):
    output1 = f"test4输出1: {input1} ** 2"
    output2 = f"test4输出2: {input2} ** 3"
    output3 = f"test4输出3: {input1} + {input2} ** 4"
    return output1, output2, output3

def freeFallSimu(input1, input2):
    FreeFall(9.81, input1, input2).freeFall()


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
        if method == timeDomainSimu:
            out1, out2, out3, out4, out5, out6 = method(*input_values)
            # 更新输出框内容
            output1.config(text=out1)
            output2.config(text=out2)
            output3.config(text=out3)
            output4.config(text=out4)
            output5.config(text=out5)
            output6.config(text=out6)

            # 读取并显示第一张plot图
            img1 = Image.open('pic/TimeDomain/step_response.png')
            img1 = img1.resize((550, 550))  # 调整图片大小
            img1_tk = ImageTk.PhotoImage(img1)
            img_label1 = tk.Label(new_window, image=img1_tk)
            img_label1.image = img1_tk  # 避免图片被回收
            img_label1.pack(side=tk.LEFT)
            # 读取并显示第二张plot图
            img2 = Image.open('pic/TimeDomain/ramp_response.png')  # 假设这是斜坡响应的图片文件名
            img2 = img2.resize((550, 550))
            img2_tk = ImageTk.PhotoImage(img2)
            img_label2 = tk.Label(new_window, image=img2_tk)
            img_label2.image = img2_tk
            img_label2.pack(side=tk.RIGHT)

        elif method == rootLocusSimu:
            method(*input_values)
            # 读取并显示第一张plot图
            img1 = Image.open('pic/RootLocus/rootLocus.png')
            img1 = img1.resize((550, 550))  # 调整图片大小
            img1_tk = ImageTk.PhotoImage(img1)
            img_label1 = tk.Label(new_window, image=img1_tk)
            img_label1.image = img1_tk  # 避免图片被回收
            img_label1.pack(side=tk.LEFT)
            # 读取并显示第二张plot图
            img2 = Image.open('pic/RootLocus/step_response.png')
            img2 = img2.resize((550, 550))
            img2_tk = ImageTk.PhotoImage(img2)
            img_label2 = tk.Label(new_window, image=img2_tk)
            img_label2.image = img2_tk
            img_label2.pack(side=tk.RIGHT)
        elif method == frequencyDomainSimu:
            out1, out2, out3, out4 = method(*input_values)
            # 更新输出框内容
            output1.config(text=out1)
            output2.config(text=out2)
            output3.config(text=out3)
            output4.config(text=out4)
            # 读取并显示第一张plot图
            img1 = Image.open('pic/FrequencyDomain/BodePlot.png')
            img1 = img1.resize((550, 550))  # 调整图片大小
            img1_tk = ImageTk.PhotoImage(img1)
            img_label1 = tk.Label(new_window, image=img1_tk)
            img_label1.image = img1_tk  # 避免图片被回收
            img_label1.pack(side=tk.LEFT)
            # 读取并显示第二张plot图
            img2 = Image.open('pic/FrequencyDomain/NyquistPlot.png')
            img2 = img2.resize((550, 550))
            img2_tk = ImageTk.PhotoImage(img2)
            img_label2 = tk.Label(new_window, image=img2_tk)
            img_label2.image = img2_tk
            img_label2.pack(side=tk.RIGHT)
        elif method == checkSimu:
            out1, out2, out3 = method(*input_values)
        elif method == freeFallSimu:
            method(*input_values)
            img1 = Image.open('pic/FreeFall/freeFall.png')
            img1 = img1.resize((550, 550))  # 调整图片大小
            img1_tk = ImageTk.PhotoImage(img1)
            img_label1 = tk.Label(new_window, image=img1_tk)
            img_label1.image = img1_tk  # 避免图片被回收
            img_label1.pack(side=tk.LEFT)
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
    ("时域仿真设计", timeDomainSimu, ["输入分子:", "输入分母:"], "1200x800", 25),
    ("根轨迹仿真设计", rootLocusSimu, ["输入分子:", "输入分母:", "开环增益:"], "1200x800", 25),
    ("频域仿真设计", frequencyDomainSimu, ["输入分子:", "输入分母:"], "1200x800", 25),
    ("校正仿真设计", checkSimu, ["输入M:", "输入N:"], "1200x800", 25),
    ("重力加速度", freeFallSimu, ["最大时间:", "时间步长:"], "1200x800", 25)
]

for title, method, input_labels, window_size, button_width in buttons:
    button = tk.Button(root, text=title, width=button_width, command=lambda method=method, title=title, input_labels=input_labels, window_size=window_size: create_interface(root, method, title, input_labels, window_size))
    button.pack(pady=5)  # 添加垂直间距

# 运行主循环
root.mainloop()