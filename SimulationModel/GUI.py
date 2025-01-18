import tkinter as tk
from tkinter import Toplevel
import numpy as np
from PIL import Image, ImageTk

from RootLocus import RootLocus
from FrequencyDomain import FrequencyDomain
from FreeFall import FreeFall
from Compensation import Compensation
from MassSpringDamper import MassSpringDamper
from TimeDomainAnalysis import TimeDomainAnalysis
from DCMotor import DCMotor


# 定义四个不同的方法
def timeDomainSimu(input1, input2):
    # "25"  "1 6 25"
    rise_time, peak_time, overshoot, settling_time, dampingRatio, naturalFrequency = TimeDomainAnalysis(input1,
                                                                                                        input2).timeDomainAnalysis()

    output1 = f"上升时间: {rise_time:.5f} 秒" if not np.isnan(rise_time) else "上升时间: 未找到"
    output2 = f"峰值时间: {peak_time:.5f} 秒"
    output3 = f"超调量: {overshoot:.5f} %"
    output4 = f"调节时间（±2%范围内）: {settling_time:.5f} 秒" if not np.isnan(settling_time) else "调节时间: 未找到"
    output5 = f"阻尼比: {dampingRatio:.2f}"
    output6 = f"自然振荡频率: {naturalFrequency:.2f}"
    return [output1, output2, output3, output4, output5, output6]


def rootLocusSimu(input1, input2, input3):
    # "1", "1 3 2 0", 10
    RootLocus(input1, input2, input3).rootLocus()
    return []


def frequencyDomainSimu(input1, input2):
    # "10", "1 6 5 0"
    gm, pm, wcg, wcp = FrequencyDomain(input1, input2).frequencyDomain()
    output1 = f"幅值裕度：", {round(gm, 2)}, "dB"
    output2 = f"相角裕度：", {round(pm, 4)}, "度"
    output3 = f"幅值交叉频率频率：", {round(wcg, 4)}, "rad/s"
    output4 = f"相角原始截止频率：", {round(wcp, 4)}, "rad/s"
    return [output1, output2, output3, output4]


def compensationSimu(input1, input2, input3, compensation_type='lead'):
    if compensation_type == 'lead':
        # "100" "0.001 0.11 1 0"  "20"
        pm, wcp, pm_lead, wcp_lead, num_lead, den_lead = Compensation(input1, input2, input3).leadCompensation()
        output1 = f"原始系统相角裕度：{round(pm, 4)}度"
        output2 = f"原始系统相角交叉频率：{round(wcp, 4)}rad/s"
        output3 = f"超前校正后相角裕度：{round(pm_lead, 4)} 度"
        output4 = f"超前校正后相角交叉频率：{round(wcp_lead, 4)} rad/s"
        output5 = f"超前校正装置分子：{num_lead}"
        output6 = f"超前校正装置分母：{den_lead}"
        return [output1, output2, output3, output4, output5, output6]
    elif compensation_type == 'lag':
        # "300" "0.2 1 0"  "40"
        pm, wcp, pm_lag, wcp_lag, num_lag, den_lag = Compensation("300", "0.2 1 0", "40").lagCompensation()
        output1 = f"原始系统相角裕度：{round(pm, 4)}度"
        output2 = f"原始系统相角交叉频率：{round(wcp, 4)}rad/s"
        output3 = f"滞后校正后相角裕度：{round(pm_lag, 4)} 度"
        output4 = f"滞后校正后相角交叉频率：{round(wcp_lag, 4)} rad/s"
        output5 = f"滞后校正装置分子：{num_lag}"
        output6 = f"滞后校正装置分母：{den_lag}"
        return [output1, output2, output3, output4, output5, output6]


def freeFallSimu(input1, input2):
    FreeFall(9.81, input1, input2).freeFall()
    return []


def massSpringDamper(input1, input2, input3):
    MassSpringDamper(input1, input2, input3).massSpringDamper()
    return []


def dcMotor(input1, input2, input3, input4, input5, input6, input7, input8, input9, input10, input11, input12):
    DCMotor(input1, input2, input3, input4, input5, input6, input7, input8, input9, input10, input11, input12).dcMotor()
    return []


# 创建通用界面模板
def create_interface(root, method, title, input_labels, input_widths, window_size, layout='default'):
    new_window = Toplevel(root)
    new_window.title(title)
    new_window.geometry(window_size)  # 设置窗口大小

    # 创建输入框
    inputs = []
    if layout == 'grid':
        # 使用Grid布局管理器
        row = 0
        col = 0

        # 第一行：4个输入框，前缀为“直流电机调速模型参数”
        tk.Label(new_window, text="直流电机调速模型参数").grid(row=row, column=0, columnspan=8, sticky='w', padx=5,
                                                               pady=5)
        row += 1
        for i in range(3):
            label_text = input_labels[i]
            input_label = tk.Label(new_window, text=label_text)
            input_label.grid(row=row, column=col, sticky='w', padx=5, pady=5)
            input_entry = tk.Entry(new_window, width=input_widths[i])
            input_entry.grid(row=row, column=col + 1, padx=5, pady=5)
            inputs.append(input_entry)
            col += 2
        row += 1
        col = 0

        # 第二行：3个输入框，前缀为空格对齐
        tk.Label(new_window, text="   ").grid(row=row, column=0, columnspan=6, sticky='w', padx=5, pady=5)
        for i in range(3, 6):
            label_text = input_labels[i]
            input_label = tk.Label(new_window, text=label_text, anchor='e')
            input_label.grid(row=row, column=col, sticky='w', padx=5, pady=5)
            input_entry = tk.Entry(new_window, width=input_widths[i])
            input_entry.grid(row=row, column=col + 1, padx=5, pady=5)
            inputs.append(input_entry)
            col += 2
        row += 1
        col = 0

        # 第三行：4个输入框，前缀为“PID补偿器参数”
        tk.Label(new_window, text="PID补偿器参数").grid(row=row, column=0, columnspan=8, sticky='w', padx=5, pady=5)
        row += 1
        pid_values = [1, 0.8, 0.01]  # 预输入值
        for i in range(6, 9):
            label_text = input_labels[i]
            input_label = tk.Label(new_window, text=label_text, anchor='e')
            input_label.grid(row=row, column=col, sticky='w', padx=5, pady=5)
            input_entry = tk.Entry(new_window, width=input_widths[i])
            input_entry.grid(row=row, column=col + 1, padx=5, pady=5)
            input_entry.insert(0, pid_values[i - 6])  # 插入预输入值
            inputs.append(input_entry)
            col += 2
        row += 1
        col = 0

        # 第四行：3个输入框，前缀为“定义仿真参数”
        tk.Label(new_window, text="定义仿真参数").grid(row=row, column=0, columnspan=6, sticky='w', padx=5, pady=5)
        row += 1
        for i in range(9, 12):
            label_text = input_labels[i]
            input_label = tk.Label(new_window, text=label_text, anchor='e')
            input_label.grid(row=row, column=col, sticky='w', padx=5, pady=5)
            input_entry = tk.Entry(new_window, width=input_widths[i])
            input_entry.grid(row=row, column=col + 1, padx=5, pady=5)
            inputs.append(input_entry)
            col += 2
    elif layout == 'default':
        # 使用Pack布局管理器
        for label_text, width in zip(input_labels, input_widths):
            input_label = tk.Label(new_window, text=label_text)
            input_label.pack()
            input_entry = tk.Entry(new_window, width=width)
            input_entry.pack()
            inputs.append(input_entry)

    # 定义按钮点击事件
    def on_button_click(compensation_type=None):
        # 清除上一次的输出
        for widget in output_frame.winfo_children():
            widget.destroy()
        for widget in image_frame.winfo_children():
            widget.destroy()
        # 获取输入值
        input_values = [input_entry.get() for input_entry in inputs]
        # 调用方法并获取输出
        if method == timeDomainSimu:
            outputs = method(*input_values)
            # 动态创建输出框并更新内容
            for output in outputs:
                output_label = tk.Label(output_frame, text=output)
                output_label.pack()
            # 读取并显示第一张plot图
            img1 = Image.open('pic/TimeDomain/step_response.png')
            img1 = img1.resize((500, 400))  # 调整图片大小
            img1_tk = ImageTk.PhotoImage(img1)
            img_label1 = tk.Label(image_frame, image=img1_tk)
            img_label1.image = img1_tk  # 避免图片被回收
            img_label1.pack(side=tk.LEFT)
            # 读取并显示第二张plot图
            img2 = Image.open('pic/TimeDomain/ramp_response.png')  # 假设这是斜坡响应的图片文件名
            img2 = img2.resize((500, 400))
            img2_tk = ImageTk.PhotoImage(img2)
            img_label2 = tk.Label(image_frame, image=img2_tk)
            img_label2.image = img2_tk
            img_label2.pack(side=tk.RIGHT)
        elif method == rootLocusSimu:
            outputs = method(*input_values)
            # 动态创建输出框并更新内容
            for output in outputs:
                output_label = tk.Label(output_frame, text=output)
                output_label.pack()
            # 读取并显示第一张plot图
            img1 = Image.open('pic/RootLocus/rootLocus.png')
            img1 = img1.resize((500, 400))  # 调整图片大小
            img1_tk = ImageTk.PhotoImage(img1)
            img_label1 = tk.Label(image_frame, image=img1_tk)
            img_label1.image = img1_tk  # 避免图片被回收
            img_label1.pack(side=tk.LEFT)
            # 读取并显示第二张plot图
            img2 = Image.open('pic/RootLocus/step_response.png')
            img2 = img2.resize((500, 400))
            img2_tk = ImageTk.PhotoImage(img2)
            img_label2 = tk.Label(image_frame, image=img2_tk)
            img_label2.image = img2_tk
            img_label2.pack(side=tk.RIGHT)
        elif method == frequencyDomainSimu:
            outputs = method(*input_values)
            # 动态创建输出框并更新内容
            for output in outputs:
                output_label = tk.Label(output_frame, text=output)
                output_label.pack()
            # 读取并显示第一张plot图
            img1 = Image.open('pic/FrequencyDomain/BodePlot.png')
            img1 = img1.resize((500, 400))  # 调整图片大小
            img1_tk = ImageTk.PhotoImage(img1)
            img_label1 = tk.Label(image_frame, image=img1_tk)
            img_label1.image = img1_tk  # 避免图片被回收
            img_label1.pack(side=tk.LEFT)
            # 读取并显示第二张plot图
            img2 = Image.open('pic/FrequencyDomain/NyquistPlot.png')
            img2 = img2.resize((500, 400))
            img2_tk = ImageTk.PhotoImage(img2)
            img_label2 = tk.Label(image_frame, image=img2_tk)
            img_label2.image = img2_tk
            img_label2.pack(side=tk.RIGHT)
        elif method == compensationSimu:
            outputs = method(*input_values, compensation_type)
            # 动态创建输出框并更新内容
            for output in outputs:
                output_label = tk.Label(output_frame, text=output)
                output_label.pack()
            if compensation_type == 'lead':
                img1 = Image.open('pic/Compensation/lead/Original.png')
                img1 = img1.resize((500, 400))  # 调整图片大小
                img1_tk = ImageTk.PhotoImage(img1)
                img_label1 = tk.Label(image_frame, image=img1_tk)
                img_label1.image = img1_tk  # 避免图片被回收
                img_label1.pack(side=tk.LEFT)
                # 读取并显示第二张plot图
                img2 = Image.open('pic/Compensation/lead/LeadCompensated.png')
                img2 = img2.resize((500, 400))
                img2_tk = ImageTk.PhotoImage(img2)
                img_label2 = tk.Label(image_frame, image=img2_tk)
                img_label2.image = img2_tk
                img_label2.pack(side=tk.RIGHT)
            elif compensation_type == 'lag':
                img1 = Image.open('pic/Compensation/lag/Original.png')
                img1 = img1.resize((500, 400))  # 调整图片大小
                img1_tk = ImageTk.PhotoImage(img1)
                img_label1 = tk.Label(image_frame, image=img1_tk)
                img_label1.image = img1_tk  # 避免图片被回收
                img_label1.pack(side=tk.LEFT)
                # 读取并显示第二张plot图
                img2 = Image.open('pic/Compensation/lag/LagCompensated.png')
                img2 = img2.resize((500, 400))
                img2_tk = ImageTk.PhotoImage(img2)
                img_label2 = tk.Label(image_frame, image=img2_tk)
                img_label2.image = img2_tk
                img_label2.pack(side=tk.RIGHT)
        elif method == freeFallSimu:
            outputs = method(*input_values)
            # 动态创建输出框并更新内容
            for output in outputs:
                output_label = tk.Label(output_frame, text=output)
                output_label.pack()
            img = Image.open('pic/FreeFall/freeFall.png')
            img = img.resize((500, 400))  # 调整图片大小
            img_tk = ImageTk.PhotoImage(img)
            img_label = tk.Label(image_frame, image=img_tk)
            img_label.image = img_tk  # 避免图片被回收
            img_label.pack(side=tk.LEFT)
        elif method == massSpringDamper:
            outputs = method(*input_values)
            # 动态创建输出框并更新内容
            for output in outputs:
                output_label = tk.Label(output_frame, text=output)
                output_label.pack()
            img = Image.open('pic/MassSpringDamper/massSpringDamper.png')
            img = img.resize((500, 400))  # 调整图片大小
            img_tk = ImageTk.PhotoImage(img)
            img_label = tk.Label(image_frame, image=img_tk)
            img_label.image = img_tk  # 避免图片被回收
            img_label.pack(side=tk.LEFT)
        elif method == dcMotor:
            outputs = method(*input_values)
            # 动态创建输出框并更新内容
            for output in outputs:
                output_label = tk.Label(output_frame, text=output)
                output_label.pack()
            # 读取并显示第一张plot图
            img = Image.open('pic/DCMotor/dcMotor.png')
            img = img.resize((500, 400))  # 调整图片大小
            img1_tk = ImageTk.PhotoImage(img)
            img_label = tk.Label(image_frame, image=img1_tk)
            img_label.image = img1_tk  # 避免图片被回收
            img_label.pack()

    # 创建按钮
    if method == timeDomainSimu:
        button_time = tk.Button(new_window, text="时域分析", command=on_button_click)
        button_time.pack()
    elif method == rootLocusSimu:
        button_root = tk.Button(new_window, text="根轨迹", command=on_button_click)
        button_root.pack()
    elif method == frequencyDomainSimu:
        button_freq = tk.Button(new_window, text="频域分析", command=on_button_click)
        button_freq.pack()
    elif method == compensationSimu:
        button_lead = tk.Button(new_window, text="超前校正", command=lambda: on_button_click('lead'))
        button_lead.pack()
        button_lag = tk.Button(new_window, text="滞后校正", command=lambda: on_button_click('lag'))
        button_lag.pack()
    elif method == freeFallSimu:
        button_fall = tk.Button(new_window, text="自由落体仿真设计", command=on_button_click)
        button_fall.pack()
    elif method == massSpringDamper:
        button_mess = tk.Button(new_window, text="质量弹簧阻尼器系统", command=on_button_click)
        button_mess.pack()
    elif method == dcMotor:
        # 换行显示按钮
        row += 1  # 更新行号，让按钮换行显示
        col = 0  # 重置列号，让按钮从新的一行的开始位置显示
        button_dc = tk.Button(new_window, text="直流电机仿真设计", command=on_button_click)
        button_dc.grid(row=row, column=col, padx=5, pady=5, columnspan=8)

    # 创建输出框
    if method == dcMotor:
        # 创建输出框容器
        output_frame = tk.Frame(new_window)
        output_frame.grid(pady=10)
        # 创建图片容器
        image_frame = tk.Frame(new_window)
        image_frame.grid(pady=10, columnspan=8)
    else:
        output_frame = tk.Frame(new_window)
        output_frame.pack(pady=10)
        # 创建图片容器
        image_frame = tk.Frame(new_window)
        image_frame.pack(pady=10)


# 创建主窗口
root = tk.Tk()
root.title("主界面")
root.geometry("800x600")

# 创建四个选项按钮
buttons = [
    ("时域仿真设计", timeDomainSimu, ["分子:", "分母:"], [20, 20], "1100x800", 25, 'default'),
    ("根轨迹仿真设计", rootLocusSimu, ["分子:", "分母:", "开环增益:"], [20, 20, 20], "1100x800", 25, 'default'),
    ("频域仿真设计", frequencyDomainSimu, ["分子:", "输入分母:"], [20, 20], "1100x800", 25, 'default'),
    ("校正仿真设计", compensationSimu, ["分子:", "分母:", "目标裕度:"], [20, 20, 20], "1100x800", 25, 'default'),
    ("自由落体仿真设计", freeFallSimu, ["最大时间:", "时间步长:"], [20, 20], "1100x800", 25, 'default'),
    ("质量弹簧阻尼系统", massSpringDamper, ["质量:", "弹簧常数:", "阻尼系数:"], [20, 20, 20], "1100x800", 25, 'default'),
    ("直流电机仿真设计", dcMotor,
     ["电枢电阻（欧姆）:", "电枢电感（亨利）:", "电机转矩常数（N·m/A）:", "电机反电动势常数（V·s/rad）:",
      "电机转子转动惯量（kg·m²）:", "电机转子粘滞摩擦系数（N·m·s/rad）:", "比例增益P:", "积分增益I:", "微分增益D:",
      "仿真时间（秒）:", "时间步长（秒）:", "目标转速（rad/s）:"],
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], "1100x800", 25, 'grid')
]

for title, method, input_labels, input_widths, window_size, button_width, layout in buttons:
    button = tk.Button(root, text=title, width=button_width,
                       command=lambda method=method, title=title, input_labels=input_labels, input_widths=input_widths,
                                      window_size=window_size, layout=layout:
                       create_interface(root, method, title, input_labels, input_widths, window_size, layout))
    button.pack(pady=5)  # 添加垂直间距

# 运行主循环
root.mainloop()
