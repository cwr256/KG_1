import pandas as pd

# 读取原始Excel文件
file_path = '学生基本信息wp.xlsx'
df = pd.read_excel(file_path)

# 处理住宿安排列，只保留第一个“-”前的字
df['住宿安排'] = df['住宿安排'].apply(lambda x: x.split('-')[0] if isinstance(x, str) else x)

# 保留需要的列
df = df[['姓名', '性别', '班级', '专业', '住宿安排']]

# 保存到一个新的CSV文件
new_file_path = 'students_all_classes.csv'
df.to_csv(new_file_path, index=False, encoding='utf-8-sig')
