import os

# 目录路径
directory = 'allclasscsv'  # 请替换为实际路径
# 输出Cypher代码的文件路径
output_file = 'KG_prj_cypher_coding.txt'

# 模板Cypher代码
cypher_template = '''
LOAD CSV WITH HEADERS FROM 'file:///{filename}' AS row
MATCH (student:StudentName {{name: row.姓名}})
// 关联学生节点和性别节点
WITH row, student
MATCH (gender:Gender {{type: row.性别}})
MERGE (student)-[:性别]->(gender)

// 关联学生节点和宿舍名称节点
WITH row, student
MATCH (dormName:DormName {{name: row.住宿安排}})
MERGE (student)-[:入住]->(dormName)

// 关联学生节点和专业名称节点
WITH row, student
MATCH (professionName:ProfessionName {{name: row.专业}})
MERGE (student)-[:所学专业]->(professionName)

// 关联学生节点和班级节点
WITH row, student
MATCH (className:Class {{name: row.班级}})
MERGE (student)-[:所在班级]->(className)
'''

# 获取所有CSV文件名
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

# 生成Cypher代码并写入文件
with open(output_file, 'w', encoding='utf-8') as f:
    for csv_file in csv_files:
        cypher_code = cypher_template.format(filename=csv_file)
        f.write(cypher_code + '\n\n')

print(f"Cypher commands have been written to {output_file}")
