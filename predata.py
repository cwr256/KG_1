import pandas as pd

# 读取原始Excel文件
file_path = '学生基本信息wp.xlsx'
df = pd.read_excel(file_path)

# 遍历所有班级并保存到不同的CSV文件中
for class_name, group in df.groupby('班级'):
    # 处理住宿安排列，只保留第一个“-”前的字
    group['住宿安排'] = group['住宿安排'].apply(lambda x: x.split('-')[0] if isinstance(x, str) else x)

    # 保留需要的列
    group = group[['姓名', '性别', '班级', '专业', '住宿安排']]

    # 保存到新的CSV文件
    new_file_path = f'students{class_name}.csv'
    group.to_csv(new_file_path, index=False, encoding='utf-8-sig')


