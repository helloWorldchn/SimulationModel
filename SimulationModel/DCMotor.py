import numpy as np
import matplotlib.pyplot as plt


class DCMotor:
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False

    def __init__(self, R=1.0, L=0.1, Kt=0.5, Ke=0.5, J=0.01, B=0.01, Kp=1, Ki=0.8, Kd=0.01, t_max=10, dt=0.01,
                 omega_ref=2000) -> None:
        """
        直流电机仿真系统
        :param R: 电枢电阻（欧姆）
        :param L: 电枢电感（亨利）
        :param Kt: 电机转矩常数（N·m/A）
        :param Ke: 电机反电动势常数（V·s/rad）
        :param J: 电机转子转动惯量（kg·m²）
        :param B: 电机转子粘滞摩擦系数（N·m·s/rad）
        :param Kp:  比例增益
        :param Ki: 积分增益
        :param Kd: 微分增益
        :param t_max: 仿真时间（秒）
        :param dt: 时间步长（秒）
        :param omega_ref: 目标转速（rad/s）
        """
        # 定义直流电机调速模型参数
        self.R = float(R)  # 电枢电阻（欧姆）
        self.L = float(L)  # 电枢电感（亨利）
        self.Kt = float(Kt)  # 电机转矩常数（N·m/A）
        self.Ke = float(Ke)  # 电机反电动势常数（V·s/rad）
        self.J = float(J)  # 电机转子转动惯量（kg·m²）
        self.B = float(B)  # 电机转子粘滞摩擦系数（N·m·s/rad）
        # 定义PID补偿器参数
        self.Kp = float(Kp)  # 比例增益
        self.Ki = float(Ki)  # 积分增益
        self.Kd = float(Kd)  # 微分增益
        # 定义仿真参数
        self.t_max = float(t_max)  # 仿真时间（秒）
        self.dt = float(dt)  # 时间步长（秒）
        # 定义目标转速（这里以恒定目标转速为例）
        self.omega_ref = float(omega_ref)  # 目标转速（rad/s）

    def dcMotor(self):
        # 定义直流电机调速模型参数
        R = self.R  # 电枢电阻（欧姆）
        L = self.L  # 电枢电感（亨利）
        Kt = self.Kt  # 电机转矩常数（N·m/A）
        Ke = self.Ke  # 电机反电动势常数（V·s/rad）
        J = self.J  # 电机转子转动惯量（kg·m²）
        B = self.B  # 电机转子粘滞摩擦系数（N·m·s/rad）

        # 定义PID补偿器参数
        Kp = self.Kp  # 比例增益
        Ki = self.Ki  # 积分增益
        Kd = self.Kd  # 微分增益
        Kc = 2.5  # 电流反馈增益

        # 定义仿真参数
        t_max = self.t_max  # 仿真时间（秒）
        dt = self.dt  # 时间步长（秒）
        t = np.arange(0, t_max, dt)  # 时间数组

        # 定义目标转速（这里以恒定目标转速为例）
        omega_ref = self.omega_ref  # 目标转速（rad/s）

        # 初始化电机状态变量和PID补偿器变量
        i = 0  # 电枢电流（A）
        omega = 0  # 电机转速（rad/s）
        integral_error = 0  # 积分误差
        prev_error = 0  # 上一次的误差

        # 初始化输出数组
        omega_arr = np.zeros_like(t)
        i_arr = np.zeros_like(t)

        i_arr[0] = 0

        # 仿真循环
        for k in range(1, len(t)):
            # 计算转速误差
            error = omega_ref - omega
            # 计算积分误差
            integral_error += error * dt
            # 计算微分误差
            derivative_error = (error - prev_error) / dt
            # 计算PID补偿器输出（控制电压）
            V = Kp * error + Ki * integral_error + Kd * derivative_error - Kc * i

            # 计算电枢电流变化率
            di_dt = (V - R * i - Ke * omega) / L
            # 计算电机转速变化率
            domega_dt = (Kt * i - B * omega) / J
            # 更新电枢电流和电机转速
            i += di_dt * dt
            omega += domega_dt * dt
            # 存储电机转速和电枢电流
            omega_arr[k] = omega
            i_arr[k] = i
            # 更新上一次的误差
            prev_error = error

        # 绘制转速和电流曲线图
        plt.figure(figsize=(12, 6))

        plt.subplot(2, 1, 1)
        plt.plot(t, omega_arr, label='实际转速')
        plt.axhline(y=omega_ref, color='r', linestyle='--', label='目标转速')
        plt.xlabel('时间（s）')
        plt.ylabel('转速（rad/s）')
        plt.title('直流电机调速模型转速曲线')
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.plot(t, i_arr)
        plt.xlabel('时间（s）')
        plt.ylabel('电流（A）')
        plt.title('直流电机调速模型电流曲线')
        plt.tight_layout()
        plt.savefig('pic/DCMotor/dcMotor.png')
        plt.show()


if __name__ == '__main__':
    DCMotor(R=1.0, L=0.1, Kt=0.5, Ke=0.5, J=0.01, B=0.01, Kp=1, Ki=0.8, Kd=0.01, t_max=10, dt=0.01, omega_ref=2000).dcMotor()
