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

cursor.execute("DELETE FROM lines")

# 打开 JSON 文件并插入数据
with open('src/lines.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    # 插入数据
    for item in data.keys():
        line_name = item
        start_time = data[item]['start_time']
        end_time = data[item]['end_time']
        intro = data[item]['intro']
        mileage = data[item]['mileage']
        color = data[item]['color']
        first_opening = data[item]['first_opening']
        url = data[item]['url']

        # 执行插入操作
        cursor.execute(
            "INSERT INTO lines (line_name, start_time, end_time, intro, mileage,color,first_opening,url) VALUES (%s, %s, %s,%s,%s,%s,%s,%s)",
            (line_name, start_time, end_time, intro, mileage,color,first_opening,url))


# 提交事务
conn.commit()

# 关闭连接
cursor.close()
conn.close()
