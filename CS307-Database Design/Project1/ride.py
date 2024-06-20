# import time
# from itertools import count
#
# import psycopg2
# import json
# from datetime import datetime
# # 连接到 PostgreSQL 数据库
#
# conn = psycopg2.connect(
#     dbname="project1",
#     user="postgres",
#     password="123456789Bw&",
#     host="localhost",
#     port="5432"
# )
# cursor = conn.cursor()
#
# cursor.execute("DELETE FROM passenger_ride")
# cursor.execute("DELETE FROM card_ride")
#
# counter_passenger = count(start=1)
# counter_card = count(start=1)
#
# # 打开 JSON 文件并插入数据
# with open('src/ride.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
#
# start = time.time()
# # 插入数据
# for item in data:
#     user_id = item['user']
#     start_station = item['start_station']
#     end_station = item['end_station']
#     price = item['price']
#     start_time = item['start_time']
#     end_time = item['end_time']
#     # 如果是U那么就是人的id
#     if len(user_id) == 18:
#         passenger_ride_id = next(counter_passenger)
#         cursor.execute(
#             "INSERT INTO passenger_ride (ride_id,passenger_id,start_station,end_station,price,start_time,end_time) VALUES (%s,%s, %s,%s,%s, %s,%s)",
#             (passenger_ride_id, user_id, start_station, end_station, price, start_time, end_time))
#     else:
#         card_ride_id = next(counter_card)
#         cursor.execute(
#             "INSERT INTO card_ride (ride_id,card_id,start_station,end_station,price,start_time,end_time) VALUES (%s,%s, %s,%s,%s, %s,%s)",
#             (card_ride_id, user_id, start_station, end_station, price, start_time, end_time))
#
# end = time.time()
# print("Loading speed =", len(data) / (end - start), "records/s")
#
# with open('time.txt','a') as file:
#     file.write(f"Loading speed by PostgreSQL (insert one by one): {len(data) / (end - start)} records/s\n")
#
# # 提交事务
# conn.commit()
#
# # 关闭连接
# cursor.close()
# conn.close()

##---------------------------------------------------------分批次-----------------------------------------------------

# import time
# from itertools import count
#
# import psycopg2
# import json
# from datetime import datetime
#
# # 连接到 PostgreSQL 数据库
# conn = psycopg2.connect(
#     dbname="project1",
#     user="postgres",
#     password="123456789Bw&",
#     host="localhost",
#     port="5432"
# )
# cursor = conn.cursor()
#
# cursor.execute("DELETE FROM passenger_ride")
# cursor.execute("DELETE FROM card_ride")
#
# counter_passenger = count(start=1)
# counter_card = count(start=1)
#
# # 打开 JSON 文件并插入数据
# with open('src/ride.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
#
# passenger_data = []
# card_data = []
# start = time.time()
#
# for item in data:
#     user_id = item['user']
#     start_station = item['start_station']
#     end_station = item['end_station']
#     price = item['price']
#     start_time = item['start_time']
#     end_time = item['end_time']
#     if len(user_id) == 18:
#         passenger_ride_id = next(counter_passenger)
#         passenger_data.append((passenger_ride_id,user_id, start_station, end_station, price, start_time, end_time))
#     else:
#         card_ride_id = next(counter_card)
#         card_data.append((card_ride_id,user_id, start_station, end_station, price, start_time, end_time))
#
# # 批量插入数据
# cursor.executemany(
#     "INSERT INTO passenger_ride (ride_id,passenger_id,start_station,end_station,price,start_time,end_time) VALUES (%s,%s,%s,%s,%s,%s,%s)",
#     passenger_data
# )
#
# cursor.executemany(
#     "INSERT INTO card_ride (ride_id,card_id,start_station,end_station,price,start_time,end_time) VALUES (%s,%s,%s,%s,%s,%s,%s)",
#     card_data
# )
#
# end = time.time()
# print("Loading speed =", len(data) / (end - start), "records/s")
#
# with open('time.txt','a') as file:
#     file.write(f"Loading speed to PostgreSQL (insert many): {len(data) / (end - start)} records/s\n")
#
# # 提交事务
# conn.commit()
#
# # 关闭连接
# cursor.close()
# conn.close()

##-----------------------------------------------------------------copy导入---------------------------------------

import time
from itertools import count

import pandas as pd
from io import StringIO

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

cursor.execute("DELETE FROM passenger_ride")
cursor.execute("DELETE FROM card_ride")

counter_passenger = count(start=1)
counter_card = count(start=1)

# 打开 JSON 文件并插入数据
with open('src/ride.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

passenger_data = []
card_data = []
start = time.time()

for item in data:
    user_id = item['user']
    start_station = item['start_station']
    end_station = item['end_station']
    price = item['price']
    start_time = item['start_time']
    end_time = item['end_time']
    if len(user_id) == 18:
        passenger_ride_id = next(counter_passenger)
        passenger_data.append((passenger_ride_id, user_id, start_station, end_station, price, start_time, end_time))
    else:
        card_ride_id = next(counter_card)
        card_data.append((card_ride_id, user_id, start_station, end_station, price, start_time, end_time))

# 批量插入数据

passenger_datas = pd.DataFrame(passenger_data)
card_datas = pd.DataFrame(card_data)

f_passenger = StringIO()
f_card = StringIO()

passenger_datas.to_csv(f_passenger, sep='\t', index=False, header=False)
card_datas.to_csv(f_card, sep='\t', index=False, header=False)

f_passenger.seek(0)
f_card.seek(0)

cursor.copy_from(f_passenger, 'passenger_ride',
                 columns=('ride_id', 'passenger_id', 'start_station', 'end_station', 'price', 'start_time', 'end_time'))
cursor.copy_from(f_card, 'card_ride',
                 columns=('ride_id', 'card_id', 'start_station', 'end_station', 'price', 'start_time', 'end_time'))

end = time.time()
print("Loading speed =", len(data) / (end - start), "records/s")

with open('time.txt', 'a') as file:
    file.write(f"Loading speed to PostgreSQL (using copy_from): {len(data) / (end - start)} records/s\n")

# 提交事务
conn.commit()

# 关闭连接
cursor.close()
conn.close()

##---------------------------------------------------batch------------------------------------------------------

# import time
# from itertools import count
#
# import psycopg2
# import json
#
# # 连接到 PostgreSQL 数据库
# conn = psycopg2.connect(
#     dbname="project1",
#     user="postgres",
#     password="123456789Bw&",
#     host="localhost",
#     port="5432"
# )
# cursor = conn.cursor()
#
# cursor.execute("DELETE FROM passenger_ride")
# cursor.execute("DELETE FROM card_ride")
#
# counter_passenger = count(start=1)
# counter_card = count(start=1)
#
# # 打开 JSON 文件并插入数据
# with open('src/ride.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
#
# start = time.time()
#
# # 分批插入数据
# batch_size = 10000  # 调整批量大小
# passenger_data_batch = []
# card_data_batch = []
#
# for item in data:
#     user_id = item['user']
#     start_station = item['start_station']
#     end_station = item['end_station']
#     price = item['price']
#     start_time = item['start_time']
#     end_time = item['end_time']
#     if len(user_id) == 18:
#         passenger_ride_id = next(counter_passenger)
#         passenger_data_batch.append((passenger_ride_id, user_id, start_station, end_station, price, start_time, end_time))
#     else:
#         card_ride_id = next(counter_card)
#         card_data_batch.append((card_ride_id, user_id, start_station, end_station, price, start_time, end_time))
#
#     if len(passenger_data_batch) >= batch_size:
#         cursor.executemany(
#             "INSERT INTO passenger_ride (ride_id,passenger_id,start_station,end_station,price,start_time,end_time) VALUES (%s,%s,%s,%s,%s,%s,%s)",
#             passenger_data_batch
#         )
#         passenger_data_batch = []
#
#     if len(card_data_batch) >= batch_size:
#         cursor.executemany(
#             "INSERT INTO card_ride (ride_id,card_id,start_station,end_station,price,start_time,end_time) VALUES (%s,%s,%s,%s,%s,%s,%s)",
#             card_data_batch
#         )
#         card_data_batch = []
#
# # 处理剩余数据
# if passenger_data_batch:
#     cursor.executemany(
#         "INSERT INTO passenger_ride (ride_id,passenger_id,start_station,end_station,price,start_time,end_time) VALUES (%s,%s,%s,%s,%s,%s,%s)",
#         passenger_data_batch
#     )
#
# if card_data_batch:
#     cursor.executemany(
#         "INSERT INTO card_ride (ride_id,card_id,start_station,end_station,price,start_time,end_time) VALUES (%s,%s,%s,%s,%s,%s,%s)",
#         card_data_batch
#     )
#
# end = time.time()
# print("Loading speed =", len(data) / (end - start), "records/s")
#
# with open('time.txt', 'a') as file:
#     file.write(f"Loading speed by PostgreSQL (batch insert): {len(data) / (end - start)} records/s\n")
#
# # 提交事务
# conn.commit()
#
# # 关闭连接
# cursor.close()
# conn.close()

