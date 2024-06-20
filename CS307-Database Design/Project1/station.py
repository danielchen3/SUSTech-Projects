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

cursor.execute("DELETE FROM station")

# 打开 JSON 文件并插入数据
with open('src/stations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    # 插入数据
    for item in data.keys():
        station_name = item
        district = data[item]['district']
        intro = data[item]['intro']
        chinese_name = data[item]['chinese_name']

        # 执行插入操作
        cursor.execute(
            "INSERT INTO station (station_name,district,intro,chinese_name) VALUES (%s, %s, %s,%s)",
            (station_name,district,intro,chinese_name))


# 提交事务
conn.commit()

# 关闭连接
cursor.close()
conn.close()
