import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

# 读取数据
file_path = r'G:\Desktop\python项目\uuDemo\dataExcel\【AK-47 _ 卡特尔 (久经沙场)】悠悠有品近1个月-总览.xlsx'
data = pd.read_excel(file_path, header=None, names=['V1'])

# 绘制时间序列数据
plt.plot(data['V1'])
plt.show()

# 拟合ARIMA模型
model = sm.tsa.auto_arima(data['V1'], seasonal=False)
print(model.summary())

# 自定义ARL函数
def ARL():
    len_list = []

    for _ in range(10000):
        X = np.zeros(1000)
        eps = np.random.normal(0, np.sqrt(1.06), 1000)

        for i in range(2, 1000):
            X[i] = 1.6848 * X[i - 1] - 0.6848 * X[i - 2] + eps[i] + 0.8889 * eps[i - 1]

            if X[i] < -10:
                len_list.append(i)
                break

    arl = np.mean(len_list)
    return arl

# 计算ARL
arl_result = ARL()
print(f"平均运行长度 (ARL): {arl_result}")
