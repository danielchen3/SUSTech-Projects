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

cursor.execute("DELETE FROM passenger")

# 打开 JSON 文件并插入数据
with open('src/passenger.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    # 插入数据
    for item in data:
        name = item['name']
        id_number = item['id_number']
        phone_number = item['phone_number']
        gender = item['gender']
        district = item['district']

        # 执行插入操作
        cursor.execute(
            "INSERT INTO passenger (id_number, name, phone_number,gender,district) VALUES (%s, %s, %s,%s,%s)",
            (id_number, name, phone_number, gender, district))

# 提交事务
conn.commit()

# 关闭连接
cursor.close()
conn.close()
