import psycopg2
import json
from datetime import datetime

# 连接到 PostgreSQL 数据库
conn = psycopg2.connect(
    dbname="project1",
    user="postgres",
    password="123456789Bw&",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

cursor.execute("DELETE FROM card")

# 打开 JSON 文件并插入数据
with open('src/cards.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    # 插入数据
    for item in data:
        code = item['code']
        money = item['money']
        create_time = datetime.strptime(item['create_time'], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

        # 执行插入操作
        cursor.execute("INSERT INTO card (code_id, money, create_time) VALUES (%s, %s, %s )", (code, money, create_time))

# 提交事务
conn.commit()

# 关闭连接
cursor.close()
conn.close()


