import pandas as pd
import os

# 获取当前工作目录
current_directory = os.getcwd()

# 定义文件路径
file_before_path = os.path.join(current_directory, 'scorebefore.xlsx')
file_after_path = os.path.join(current_directory, 'scoreafter.xlsx')
output_file_path = os.path.join(current_directory, 'updated_after_test_data.xlsx')

# 读取Excel数据
df_before = pd.read_excel(file_before_path)
df_after = pd.read_excel(file_after_path)

# 将'X1'和'X0'列合并为新列'X'
df_before['X'] = df_before[['X1', 'X0']].mean(axis=1)

# 使用'Num'作为键，将'X'列从'前测'数据合并到'后测'数据
df_merged = pd.merge(df_after, df_before[['Num', 'X']], on='Num', how='left')

# 计算新的列'S1-X'和'S0-X'
df_merged['S1-X'] = df_merged['S1'] - df_merged['X']
df_merged['S0-X'] = df_merged['S0'] - df_merged['X']

# 将更新后的数据保存到新文件
df_merged.to_excel(output_file_path, index=False)

print(f"Updated data has been saved to: {output_file_path}")
