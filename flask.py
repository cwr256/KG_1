import jieba
from py2neo import Graph
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 尝试连接到 Neo4j 数据库
try:
    graph = Graph("bolt://127.0.0.1:7687", auth=("neo4j", "password"))
    print("成功连接到 Neo4j!")
except Exception as e:
    print("连接到 Neo4j 时出错:", e)
    raise e

# 示例问题和对应的查询模板
qa_pairs = [
    {"question": "B210416班有多少学生？",
     "template": "MATCH (c:Class {name: 'B210416'})<-[:所在班级]-(s:StudentName) RETURN COUNT(s) AS count"},
    {"question": "男生有多少？", "template": "MATCH (s:StudentName)-[:性别]->(:Gender {type: '男'}) RETURN COUNT(s) AS count"},
    {"question": "哪个学生住在宿舍1？",
     "template": "MATCH (s:StudentName)-[:入住]->(:DormName {name: '宿舍1'}) RETURN s.name AS student_name"},
    # 更多的示例和模板可以在这里添加
]

# 对示例问题进行分词
questions = [qa['question'] for qa in qa_pairs]
segmented_questions = [' '.join(jieba.cut(question)) for question in questions]

# 初始化TF-IDF向量化器
vectorizer = TfidfVectorizer()
vectorized_questions = vectorizer.fit_transform(segmented_questions)


def get_answer(user_question):
    # 对用户问题进行分词
    segmented_user_question = ' '.join(jieba.cut(user_question))

    # 向量化用户问题
    user_question_vector = vectorizer.transform([segmented_user_question])

    # 计算相似度
    similarities = cosine_similarity(user_question_vector, vectorized_questions)

    # 找到最相似的问题
    best_match_index = similarities.argmax()
    best_match_score = similarities[0, best_match_index]

    if best_match_score > 0.5:  # 设置一个相似度阈值
        best_match_qa = qa_pairs[best_match_index]
        query = best_match_qa['template']
        result = graph.run(query).data()
        return result
    else:
        return "抱歉，我无法理解您的问题。"


# 测试问答系统
user_question = "B210416有多少学生？"
answer = get_answer(user_question)
print(f"问题: {user_question}")
print(f"答案: {answer}")
