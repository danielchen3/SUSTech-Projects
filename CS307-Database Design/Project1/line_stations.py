from itertools import count

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

cursor.execute("DELETE FROM line_stations")

counter = count(start=1)

# 打开 JSON 文件并插入数据
with open('src/lines.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    # 插入数据
    for item in data.keys():
        line_name = item
        stations = data[item]['stations']

        for station in stations:
            # 执行插入操作
            id = next(counter)
            cursor.execute(
                "INSERT INTO line_stations (id,line_name,station_name) VALUES (%s,%s, %s)",
                (id, line_name, station))

# 提交事务
conn.commit()

# 关闭连接
cursor.close()
conn.close()
