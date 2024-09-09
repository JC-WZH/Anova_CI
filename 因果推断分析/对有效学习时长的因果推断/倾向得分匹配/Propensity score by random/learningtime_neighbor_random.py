import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors
import numpy as np

# 获取当前工作目录
current_dir = os.getcwd()

# 构建文件路径
input_file_path = os.path.join(current_dir, 'learningtimeafter.xlsx')
output_file_path_filled = os.path.join(current_dir, '匹配文件/learningtime_neighbor_random_results.xlsx')
output_file_path_results = os.path.join(current_dir, '匹配文件/learningtime_neighbor_random_summary.xlsx')

# 创建输出目录（如果不存在）
output_dir = os.path.dirname(output_file_path_filled)
os.makedirs(output_dir, exist_ok=True)

# 读取初始数据文件
data = pd.read_excel(input_file_path)

# Step 1: 准备数据，合并干预组（D=1）的T1值和未干预组（D=0）的T0值到一个列 'T_combined'
data['T_combined'] = np.where(data['D'] == 1, data['T1'], data['T0'])

# Step 2: 删除'T_combined'缺失的行
data_for_psm = data.dropna(subset=['T_combined'])

# Step 3: 使用逻辑回归模型计算倾向得分
X = data_for_psm[['T_combined']]  # 特征变量：合并后的学习时间数据
y = data_for_psm['D']  # 目标变量：是否接受干预（D=1或D=0）

log_reg = LogisticRegression()
log_reg.fit(X, y)

# 计算倾向得分并添加到数据中
data_for_psm['propensity_score'] = log_reg.predict_proba(X)[:, 1]

# Step 4: 将数据分为干预组（D=1）和未干预组（D=0）
treated_group = data_for_psm[data_for_psm['D'] == 1].reset_index(drop=True)
control_group = data_for_psm[data_for_psm['D'] == 0].reset_index(drop=True)

# Step 5: 匹配干预组（D=1）和未干预组（D=0），使用5个近邻
nn_treated = NearestNeighbors(n_neighbors=5)
nn_treated.fit(control_group[['propensity_score']])
distances_treated, indices_treated = nn_treated.kneighbors(treated_group[['propensity_score']])

# 检查匹配的索引和距离
print("Matched indices for treated group:")
print(indices_treated)
print("Distances for treated group:")
print(distances_treated)

# 随机选择匹配的T0值来填充D=1的T0
def get_random_matched_values(indices, values):
    return [np.random.choice(values[idx_list]) for idx_list in indices]

# 获取匹配组的索引并随机选择值
matched_control_t0 = get_random_matched_values(indices_treated, control_group['T_combined'])
treated_group['T0'] = matched_control_t0

# Step 6: 匹配未干预组（D=0）和干预组（D=1），使用5个近邻
nn_control = NearestNeighbors(n_neighbors=5)
nn_control.fit(treated_group[['propensity_score']])
distances_control, indices_control = nn_control.kneighbors(control_group[['propensity_score']])

# 检查匹配的索引和距离
print("Matched indices for control group:")
print(indices_control)
print("Distances for control group:")
print(distances_control)

# 随机选择匹配的T1值来填充D=0的T1
matched_treated_t1 = get_random_matched_values(indices_control, treated_group['T_combined'])
control_group['T1'] = matched_treated_t1

# Step 7: 合并填补后的干预组和未干预组
final_data_filled = pd.concat([treated_group, control_group])

# Step 8: 计算T1-T0并添加为新列
final_data_filled['T1-T0'] = final_data_filled['T1'] - final_data_filled['T0']

# 计算 ATT, ATE, ATU
ATT = final_data_filled[final_data_filled['D'] == 1]['T1-T0'].mean()
ATE = final_data_filled['T1-T0'].mean()
ATU = final_data_filled[final_data_filled['D'] == 0]['T1-T0'].mean()

# 创建一个DataFrame来保存计算结果
results = pd.DataFrame({
    'ATE': [ATE],
    'ATT': [ATT],
    'ATU': [ATU]
})

# 保存处理后的数据和结果到新的Excel文件
final_data_filled.to_excel(output_file_path_filled, index=False)
results.to_excel(output_file_path_results, index=False)

print(f"数据已保存到 {output_file_path_filled}")
print(f"ATT, ATE, ATU 计算结果已保存到 {output_file_path_results}")
