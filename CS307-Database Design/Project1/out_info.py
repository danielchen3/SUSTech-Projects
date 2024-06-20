import time
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

cursor.execute("DELETE FROM out_info")

counter = count(start=1)

# 打开 JSON 文件并插入数据
with open('src/stations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    start = time.time()
    # 插入数据
    for item in data.keys():
        station_name = item
        out_infos = data[item]['out_info']
        for out_info in out_infos:
            # 进行strip()删减
            id = next(counter)
            outt = out_info['outt'].strip()
            textt = out_info['textt'].strip()
            # 执行插入操作
            cursor.execute(
                "INSERT INTO out_info (id,station_name,outt,textt) VALUES (%s,%s, %s,%s)",
                (id,station_name, outt, textt))
    end = time.time()
    print("Loading speed =", (id) / (end - start), "records/s")

# 提交事务
conn.commit()

# 关闭连接
cursor.close()
conn.close()
