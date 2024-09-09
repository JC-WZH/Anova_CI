import pandas as pd
from scipy.stats import f

# 读取更新后的数据
df = pd.read_excel("updated_after_test_data.xlsx")

# 打印数据的列数和行数
print(f"Number of columns: {len(df.columns)}")
print(f"Number of rows: {len(df.index)}")

# 定义组数
r = 2

# 提取数据
data0 = df[df['D'] == 0]
Sd0 = data0['S0-X']
n0 = len(Sd0)
print(Sd0)

data1 = df[df['D'] == 1]
Sd1 = data1['S1-X']
n1 = len(Sd1)
print(Sd1)

# 计算组均值
Sd0_mean = Sd0.mean()
Sd1_mean = Sd1.mean()

# 计算总体均值
Xm = (Sd0_mean * n0 + Sd1_mean * n1) / (n0 + n1)

# 计算组间方差 (Sb2)
Sb2 = (n0 * (Sd0_mean - Xm) ** 2 + n1 * (Sd1_mean - Xm) ** 2) / (r - 1)

# 计算组内方差 (Sw2)
Sw2 = ((Sd0 - Sd0_mean) ** 2).sum() + ((Sd1 - Sd1_mean) ** 2).sum()
Sw2 /= (n0 + n1 - r)

# 计算F统计量
F = Sb2 / Sw2
print(f"F-statistic: {F:.4f}")

# 计算临界值
fenwei = f.isf(q=0.05, dfn=r - 1, dfd=n0 + n1 - r)
print(f"Critical value: {fenwei:.4f}")

# 结果解释
if F > fenwei:
    print("There is a significant difference.")
    ATE = Sd1_mean - Sd0_mean
    print(f"ATE: {ATE:.4f}; Improving rates: {ATE/Sd0_mean:.4f}")
else:
    print("There is no significant difference.")
