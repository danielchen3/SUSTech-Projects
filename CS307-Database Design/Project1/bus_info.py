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

cursor.execute("DELETE FROM bus_info")
counter = count(start=1)

# 打开 JSON 文件并插入数据
with open('src/stations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    # 插入数据
    for item in data.keys():
        station_name = item
        bus_infos = data[item]['bus_info']
        for bus_info in bus_infos:
            chukou = bus_info['chukou']
            busOutInfos = bus_info['busOutInfo']
            if (chukou.strip() != "此站暂无数据" and chukou.strip() != ""):
                for busOutInfo in busOutInfos:
                    busInfo = busOutInfo['busInfo']
                    busName = busOutInfo['busName']
                    # 执行插入操作
                    if (busName.strip() != "此站暂无数据" and busName.strip() != ""):
                        next(counter)
                        cursor.execute(
                            "INSERT INTO bus_info (busname,chukou,station_name,bus_info) VALUES (%s,%s, %s,%s)",
                            (busName, chukou, station_name, busInfo))

# 提交事务
conn.commit()

# 关闭连接
cursor.close()
conn.close()
