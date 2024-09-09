import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors
import numpy as np

# 获取当前工作目录
current_dir = os.getcwd()

# 构建文件路径
scorebefore_path = os.path.join(current_dir, 'scorebefore.xlsx')
scoreafter_path = os.path.join(current_dir, 'scoreafter.xlsx')
output_data_path = os.path.join(current_dir, '匹配文件/score_neighbor_random_results.xlsx')
output_results_path = os.path.join(current_dir, '匹配文件/score_neighbor_random_summary.xlsx')

# 创建输出目录（如果不存在）
output_dir = os.path.dirname(output_data_path)
os.makedirs(output_dir, exist_ok=True)

# 加载数据
scorebefore = pd.read_excel(scorebefore_path)  # 前测数据
scoreafter = pd.read_excel(scoreafter_path)    # 后测数据

# 根据 D 值生成新列 X
scorebefore['X'] = scorebefore.apply(lambda row: row['X1'] if row['D'] == 1 else row['X0'], axis=1)

# 合并前测和后测数据，以便正确匹配
merged_data = pd.merge(scoreafter[['Num', 'D', 'S1', 'S0']], scorebefore[['Num', 'X']], on='Num')

# 处理缺失值（用均值填充）
merged_data.fillna(merged_data.mean(), inplace=True)

# 计算倾向得分
X = merged_data[['X']]  # 使用新生成的X作为协变量
y = merged_data['D']  # 使用后测数据中的D作为因变量

model = LogisticRegression()
model.fit(X, y)
merged_data['propensity_score'] = model.predict_proba(X)[:, 1]  # 将倾向得分添加到数据中

# 区分处理组和对照组
treated_scores = merged_data[merged_data['D'] == 1].copy()
control_scores = merged_data[merged_data['D'] == 0].copy()

# 选择近邻数目
n_neighbors = 5  # 选择5个近邻
nbrs = NearestNeighbors(n_neighbors=n_neighbors)
nbrs.fit(control_scores[['propensity_score']])
distances, indices = nbrs.kneighbors(treated_scores[['propensity_score']])

# 用匹配组的后测成绩随机选择并填充
def random_match_fill(scores, indices, column):
    matched_values = []
    for index_list in indices:
        matched_values.append(np.random.choice(scores.iloc[index_list][column].values))
    return matched_values

# 对处理组D=1的S0进行随机填充
treated_scores['matched_S0'] = random_match_fill(control_scores, indices, 'S0')
merged_data.loc[merged_data['D'] == 1, 'S0'] = treated_scores['matched_S0']

# 对对照组D=0的S1进行随机填充
nbrs.fit(treated_scores[['propensity_score']])
distances, indices = nbrs.kneighbors(control_scores[['propensity_score']])
matched_S1_values = random_match_fill(treated_scores, indices, 'S1')
control_scores['matched_S1'] = matched_S1_values
merged_data.loc[merged_data['D'] == 0, 'S1'] = control_scores['matched_S1']

# 计算新列 S1-S0, S1-X, S0-X
merged_data['S1-S0'] = merged_data['S1'] - merged_data['S0']
merged_data.loc[merged_data['D'] == 1, 'S1-X'] = merged_data['S1'] - merged_data['X']
merged_data.loc[merged_data['D'] == 0, 'S0-X'] = merged_data['S0'] - merged_data['X']

# 计算 ATT, ATE, ATU
ATT = merged_data[merged_data['D'] == 1]['S1-S0'].mean()
ATE = merged_data['S1-S0'].mean()
ATU = merged_data[merged_data['D'] == 0]['S1-S0'].mean()

# 创建一个DataFrame来保存结果
results = pd.DataFrame({
    'ATE': [ATE],
    'ATT': [ATT],
    'ATU': [ATU]
})

# 保存处理后的数据和计算结果到新文件
merged_data.to_excel(output_data_path, index=False)
results.to_excel(output_results_path, index=False)

print(f"数据已保存到 {output_data_path}")
print(f"计算结果已保存到 {output_results_path}")
