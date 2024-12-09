import numpy as np
import matplotlib.pyplot as plt
from pyts.image import RecurrencePlot
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 读取Excel文件
df = pd.read_excel('force.xlsx')

df = df.rename(columns={'0W': 'Sum'})
df = df.drop(df.index[0])

# 显示前几行数据
print(df.head())

inputs = []
interval = 5000
nums = 400
start = 400000

for i in range(nums):
    time_points = df['Time'].iloc[start+i*interval:start+(i+1)*interval].values
    X1 = np.array([df['Fy'].iloc[start+i*interval:start+(i+1)*interval].values])
    X2 = np.array([df['Fz'].iloc[start+i*interval:start+(i+1)*interval].values])
    rp = RecurrencePlot(threshold=0.01)
    X_rp1 = rp.transform(X1)
    X_rp2 = rp.transform(X2)
    inputs.append(np.array([X_rp1[0].reshape(-1), X_rp2[0].reshape(-1)]).reshape(-1))
    # inputs.append(np.array([X_rp1[0].reshape(-1), X_rp2[0].reshape(-1), (X_rp1[0]+X_rp2[0]).reshape(-1)]).reshape(-1))

df_inputs = pd.DataFrame(inputs)
print(df_inputs)
outputs = np.random.randint(0, 3, nums)

# 划分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(df_inputs, outputs, test_size=0.1, random_state=42)

# 创建RandomForestClassifier实例
rf_classifier = RandomForestClassifier(n_estimators=200, random_state=42)

# 训练模型
rf_classifier.fit(X_train, y_train)

# 进行预测
y_pred = rf_classifier.predict(X_test)

# 评估模型性能
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")
