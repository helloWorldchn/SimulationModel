import control as ctrl
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 定义传递函数
numerator = [1]  # 分子系数
denominator = [1, 3, 2, 0]  # 分母系数
# 定义开环增益
openLoopGain = 10

sys = ctrl.TransferFunction(numerator, denominator)
# 计算并绘制单位阶跃响应

sys_k = sys * openLoopGain

# 绘制根轨迹
ctrl.root_locus(sys_k)
# 绘制根轨迹并获取根轨迹的值
# 绘制根轨迹并获取根轨迹的根的实部和虚部的数组
rlist, klist = ctrl.rlocus(sys_k)
# 计算根轨迹的值的数组
root_locus_values = np.array(rlist)
# 绘制根轨迹
plt.plot(root_locus_values.real, root_locus_values.imag, 'b')
plt.xlabel('实轴')
plt.ylabel('虚轴')
plt.title('根轨迹')
plt.savefig('pic/RootLocus/rootLocus.png')
plt.show()

# 计算并绘制单位阶跃响应
tStepGain, yStepGain = ctrl.step_response(sys_k)
plt.plot(tStepGain, yStepGain)
plt.xlabel('时间')
plt.ylabel('振幅')
plt.title('开环单位阶跃响应')
plt.savefig('pic/RootLocus/step_response.png')
plt.show()
