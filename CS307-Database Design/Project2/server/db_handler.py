import decimal
import json

import psycopg2
import pymysql

from config import Config

pymysql.install_as_MySQLdb()
import os
from collections import defaultdict

import networkx as nx
from flask import jsonify
from peewee import Model, CharField, TimeField, TextField, FloatField, DateField, IntegrityError, PeeweeException
from playhouse.pool import PooledPostgresqlExtDatabase, PooledMySQLDatabase

# from exceptions import AlreadyExist, NotFoundNearbyException
# from config import Config
from models import Line, Station, LineStation, PassengerRide, Passenger, Card, CardRide, BusInfo, db
from exceptions import NotFoundException, AlreadyExist
from datetime import datetime
import pandas as pd


# self.db = PooledMySQLDatabase(
#             database=Config.DATABASE_NAME,
#             user=username,
#             password=password,
#             host=Config.DATABASE_HOST,
#             port=3306,
#             max_connections=100,
#             stale_timeout=600
#         )

# Configure logging

class DatabaseHandler:
    def __init__(self, username, password):
        self.db = PooledPostgresqlExtDatabase(
            database=Config.DATABASE_NAME,
            user=username,
            password=password,
            host=Config.DATABASE_HOST,
            port=Config.DATABASE_PORT,
            max_connections=100,
            stale_timeout=600
        )
        self.db.connect()
        self.bus_lines_to_stations = defaultdict(set)

        # 构建映射
        self._build_bus_lines_to_stations_mapping()

    def close_connection(self):
        self.db.close()

    def delete_line(self, line_name):
        try:
            line = Line.get(Line.line_name == line_name)
            line.delete_instance()
            return f'Line {line_name} deleted successfully'
        except Line.DoesNotExist:
            raise NotFoundException(f'Line {line_name} not found')

    def find_line(self, line_name):
        try:
            line = Line.get(Line.line_name == line_name)
            return line.url
        except Line.DoesNotExist:
            raise NotFoundException(f'Line {line_name} not found')

    def add_line(self, line_info):
        try:
            with db.atomic():
                Line.create(
                    line_name=line_info['line_name'],
                    start_time=line_info['start_time'],
                    end_time=line_info['end_time'],
                    intro=line_info['intro'],
                    mileage=line_info['mileage'],
                    color=line_info['color'],
                    first_opening=line_info['first_opening'],
                    url=line_info['url']
                )  # 使用字典解包来设置字段值
                return f'Line {line_info["line_name"]} added successfully'
        except IntegrityError:  # 如果line_name是唯一的，并且已存在，则Peewee会抛出IntegrityError
            raise AlreadyExist(f'Line {line_info["line_name"]} already exists')

    def modify_line(self, line_info):
        try:
            with self.db.atomic():
                # 创建一个要更新的字段字典
                update_fields = {}

                if line_info['start_time'] != '/':
                    update_fields['start_time'] = line_info['start_time']
                if line_info['end_time'] != '/':
                    update_fields['end_time'] = line_info['end_time']
                if line_info['intro'] != '/':
                    update_fields['intro'] = line_info['intro']
                if line_info['mileage'] != '/':
                    update_fields['mileage'] = line_info['mileage']
                if line_info['color'] != '/':
                    update_fields['color'] = line_info['color']
                if line_info['first_opening'] != '/':
                    update_fields['first_opening'] = line_info['first_opening']
                if line_info['url'] != '/':
                    update_fields['url'] = line_info['url']

                query = Line.select().where(Line.line_name == line_info['line_name'])
                if query.count() == 0:
                    raise NotFoundException(f'Line {line_info["line_name"]} not found')
                # 如果有需要更新的字段，执行更新操作
                if update_fields:
                    query = Line.update(**update_fields).where(Line.line_name == line_info['line_name'])
                    query.execute()
                    print("Line Successfully Modified!")
                else:
                    print("No fields to update!")

        except Line.DoesNotExist:
            raise NotFoundException(f"Line {line_info['line_name']} not found")
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    def add_station(self, station_info):
        try:
            with self.db.atomic():  # 使用事务确保操作的原子性
                Station.create(
                    station_name=station_info['station_name'],
                    district=station_info['district'],
                    intro=station_info['intro'],
                    chinese_name=station_info['chinese_name'],
                )  # 使用create方法插入新记录
                return f'Station {station_info["station_name"]} added successfully'
        except IntegrityError:  # 如果station_name是唯一键，则捕获IntegrityError异常
            raise AlreadyExist(f"Station {station_info['station_name']} already exists")
        except Exception as e:  # 捕获其他可能的异常
            print(f"An error occurred: {e}")
            raise

    def delete_station(self, station_name):
        try:
            station = Station.get(Station.station_name == station_name)
            station.delete_instance()
            return f'Station {station_name} deleted successfully'
        except Station.DoesNotExist:
            raise NotFoundException(f'Station {station_name} not found')

    def modify_station(self, station_info):
        try:
            with self.db.atomic():
                # 创建一个要更新的字段字典
                update_fields = {}

                if station_info['district'] != '/':
                    update_fields['district'] = station_info['district']
                if station_info['intro'] != '/':
                    update_fields['intro'] = station_info['intro']
                if station_info['chinese_name'] != '/':
                    update_fields['chinese_name'] = station_info['chinese_name']

                query = Station.select().where(Station.station_name == station_info['station_name'])
                if query.count() == 0:
                    raise NotFoundException(f'Station {station_info["station_name"]} not found')
                # 如果有需要更新的字段，执行更新操作
                if update_fields:
                    query = Station.update(**update_fields).where(Station.station_name == station_info['station_name'])
                    query.execute()
                    print("Station Successfully Modified!")
                else:
                    print("No fields to update!")

        except Station.DoesNotExist:
            raise NotFoundException(f"Line {station_info['station_name']} not found")
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    def insert_station_before(self, line_name, before_station_name, station_name):
        try:
            with db.atomic():  # 假设db_session支持Peewee的atomic操作
                # 1. 找到要插入新站点之前的那个站点
                before_station = LineStation.get_or_none(
                    LineStation.line_name == line_name,
                    LineStation.station_name == before_station_name
                )
                print(f"before_station{before_station}")
                if before_station is None:
                    print("is_none")
                    return {'message': 'No Station'}

                # 2. 获取要插入新站点之前的站点的position值
                position_before = before_station.id

                # 3. 更新position（从指定站点开始及之后的站点都+1）
                temp_id_offset = 1000000  # 一个较大的值，假设比现有的最大ID都大
                LineStation.update(id=LineStation.id + temp_id_offset).where(
                    # (LineStation.line_name == line_name) &
                    (LineStation.id >= position_before) &  # 包括指定的站点
                    (LineStation.id.is_null(False))
                ).execute()

                # 4. 将临时值更新到最终值
                LineStation.update(id=LineStation.id - (temp_id_offset - 1)).where(
                    # (LineStation.line_name == line_name) &
                    (LineStation.id >= position_before + temp_id_offset) &
                    (LineStation.id.is_null(False))
                ).execute()

                # 4. 插入新站点
                new_position = position_before  # 使用之前站点的position值作为新站点的position
                LineStation.create(id=new_position, line_name=line_name, station_name=station_name)

        except Exception as e:
            print(f"An error occurred: {e}")

    def remove_station_from_line(self, line_name, station_name):
        try:
            with db.atomic():
                # 2. 查找并删除LineStation中对应的记录
                try:
                    line_station_to_delete = LineStation.get_or_none(
                        LineStation.line_name == line_name,
                        LineStation.station_name == station_name
                    )
                    if line_station_to_delete is None:
                        raise ValueError(f"Station '{station_name}' not found on line '{line_name}'")

                    line_deleted_id = line_station_to_delete.id

                    line_station_to_delete.delete_instance()

                    # 3. 更新剩余站点的position字段
                    temp_id_offset = 1000000  # 一个较大的值，假设比现有的最大ID都大
                    LineStation.update(id=LineStation.id + temp_id_offset).where(
                        # (LineStation.line_name == line_name) &
                        (LineStation.id > line_deleted_id) &  # 包括指定的站点
                        (LineStation.id.is_null(False))
                    ).execute()

                    # 4. 将临时值更新到最终值
                    LineStation.update(id=LineStation.id - (temp_id_offset + 1)).where(
                        # (LineStation.line_name == line_name) &
                        (LineStation.id >= line_deleted_id + temp_id_offset + 1) &
                        (LineStation.id.is_null(False))
                    ).execute()

                    print(f"Station '{station_name}' removed from line '{line_name}'.")
                except LineStation.DoesNotExist:
                    print(f"Station '{station_name}' is not in line '{line_name}'.")
        except Station.DoesNotExist:
            print(f"Station '{station_name}' not found.")
        except Line.DoesNotExist:
            print(f"Line '{line_name}' not found.")

    def find_n_stations(self, line_name, station_name, is_forward, n):
        try:
            station = LineStation.get(
                (LineStation.line_name == line_name) &
                (LineStation.station_name == station_name)
            )
            start_id = station.id

            # 计算目标ID
            if int(is_forward) == 1:
                target_id = start_id + int(n)
            else:
                # 确保目标ID不会小于1（或线路上的第一个站点的ID，如果有的话）
                target_id = start_id - int(n)

            # 尝试获取目标ID的站点
            try:
                target_station = LineStation.get(
                    (LineStation.line_name == line_name) &
                    (LineStation.id == target_id)
                )
                print(f"Target station: {target_station.station_name}")

            except target_station.DoesNotExist:
                if is_forward:
                    raise NotFoundException(
                        f"No station found {n} stations ahead of {station_name} on line {line_name}")
                else:
                    raise NotFoundException(f"No station found {n} stations behind {station_name} on line {line_name}")
            # 返回找到的站点的名称
            return target_station.station_name

        except LineStation.DoesNotExist:
            if is_forward:
                raise NotFoundException(f"No station found {n} stations ahead of {station_name} on line {line_name}")
            else:
                raise NotFoundException(f"No station found {n} stations behind {station_name} on line {line_name}")

        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    def passenger_board(self, entity_id, start_station_name):
        current_time = datetime.now()
        start_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        if len(entity_id) == 18:  # 假设乘客ID长度为18
            passenger = Passenger.get(Passenger.id_number == entity_id)
            ride_model = PassengerRide
        elif len(entity_id) == 9:  # 假设公交卡ID长度为9（仅为示例）
            card = Card.get(Card.code_id == entity_id)
            ride_model = CardRide
        else:
            raise ValueError("Invalid entity ID length")

        start_station = Station.get(Station.station_name == start_station_name)

        table_size = ride_model.select().count()

        if ride_model is PassengerRide:
            with db.atomic():
                ride = ride_model.create(
                    ride_id=table_size + 1,
                    passenger_id=entity_id,
                    start_station=start_station,
                    start_time=start_time
                )
        else:
            with db.atomic():
                ride = ride_model.create(
                    ride_id=table_size + 1,
                    card_id=entity_id,
                    start_station=start_station,
                    start_time=start_time
                )

        if ride_model is PassengerRide:
            print(f"Passenger {entity_id} boarded at {start_station.station_name} at {start_time}")
        else:
            print(f"Card {entity_id} boarded at {start_station.station_name} at {start_time}")

        return {"success": True, "message": f"Boarded successfully"}

    def passenger_alight(self, entity_id, end_station_name):
        current_time = datetime.now()
        end_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        if len(entity_id) == 18:
            passenger = Passenger.get(Passenger.id_number == entity_id)
            ride_model = PassengerRide
            id_field = PassengerRide.passenger_id
        elif len(entity_id) == 9:
            card = Card.get(Card.code_id == entity_id)
            ride_model = CardRide
            id_field = CardRide.card_id
        else:
            raise ValueError("Invalid entity ID length")

        end_station = Station.get(Station.station_name == end_station_name)
        last_ride_query = (ride_model
                           .select()
                           .where(id_field == entity_id, ride_model.end_time.is_null()))

        try:
            last_ride = last_ride_query.get()
        except ride_model.DoesNotExist:
            # raise ValueError("No ongoing ride found for the given entity ID")
            return {"Status": "False", "message": f"No ongoing ride found for the given entity ID"}

        fare = self.find_ticket_price(last_ride.start_station.chinese_name, end_station.chinese_name)

        last_ride.end_station = end_station
        last_ride.end_time = end_time
        last_ride.price = fare
        last_ride.save()

        if ride_model is PassengerRide:
            print(f"Passenger {entity_id} alighted at {end_station.station_name} at {end_time} with fare {fare}")
        else:
            print(f"Card {entity_id} alighted at {end_station.station_name} at {end_time} with fare {fare}")

        return {"Status": "True", "message": f"Alighted successfully"}

    def find_ticket_price(self, start_station, end_station):
        # 读取Excel文件
        file_path = 'src/Price.xlsx'
        df = pd.read_excel(file_path, header=None)

        # 初始化票价为None
        ticket_price = None

        # 遍历DataFrame的每一行和列，查找票价
        for index, row in df.iterrows():
            if index == 0:  # 跳过表头
                continue

                # 假设站编号在DataFrame的第二列，站名在第三列
            station_id = row[1]
            station_name = row[2]

            # 检查当前行是否是起始站
            if station_name == start_station:
                # 遍历后面的列（票价列），但注意这里我们可能需要假设票价矩阵的起始位置
                for col_index, col_value in enumerate(row[3:]):
                    # 注意：这里我们假设票价矩阵的列名在DataFrame的第三行（索引为2）
                    if df.iloc[2, col_index + 3] == end_station:
                        ticket_price = col_value
                        break

                        # 输出票价
        if ticket_price is not None:
            print(f"从{start_station}到{end_station}的票价是：{ticket_price}")
            return ticket_price
        else:
            print(f"未找到从{start_station}到{end_station}的票价。")

    metro_network = nx.Graph()

    def add_stations_and_edges_for_line(self, metro_network, line):
        stations = [s.station_name for s in LineStation.select().where(LineStation.line_name == line)]
        # print(stations)
        for station in stations:
            metro_network.add_node(station.station_name)
            # print({station})

            # 添加站点之间的边（在同一线路上，权重为1）
        for i in range(len(stations) - 1):
            start_station = stations[i]
            s1 = start_station.station_name
            end_station = stations[i + 1]
            s2 = end_station.station_name
            metro_network.add_edge(s1, s2, weight=1)
            # print(f"Added edge: {start_station} -- {end_station}")
        # 遍历所有线路并添加到图中

    def find_path(self, start_station, end_station):
        metro_network = nx.Graph()
        for line in Line.select():
            self.add_stations_and_edges_for_line(metro_network, line)
        try:
            # 使用 Dijkstra 算法找到最短路径
            shortest_path = nx.dijkstra_path(metro_network, source=start_station, target=end_station
                                             )
            return shortest_path
        except nx.NetworkXNoPath:
            # 如果没有找到路径，则返回 None 或抛出异常
            return None

    def _build_bus_lines_to_stations_mapping(self):
        # 查询所有的 BusInfo 记录
        for bus_info in BusInfo.select():
            lines = bus_info.bus_info.split(',')

            # 遍历每条公交线
            for line in lines:
                line = line.strip().split('[')[0].rstrip(']')

                # 忽略空线路或仅包含括号的线路
                if line:
                    # 将公交站名（bus_name字段）添加到对应公交线的集合中
                    self.bus_lines_to_stations[line].add(bus_info.busname)

    def find_stations_by_bus_line(self, bus_line):
        # 使用前面构建的映射返回公交站集合
        return self.bus_lines_to_stations.get(bus_line, set())

    def find_nearby_stations_by_metro_station(self, metro_station_name):
        # 查找与给定地铁站名称完全匹配的站点
        metro_stations = Station.select().where(Station.station_name == metro_station_name)

        # 如果没有找到匹配的地铁站，则返回空集合
        if not metro_stations:
            return set()

            # 假设只有一个地铁站与给定名称匹配（因为名称是唯一的）
        metro_station = metro_stations.get()

        # 初始化一个集合来存储所有找到的公交站名
        bus_names = set()

        # 查找与该地铁站点关联的所有公交信息
        bus_infos = BusInfo.select(BusInfo.busname).where(BusInfo.station == metro_station)

        # 遍历每个公交信息，并添加公交站名到集合中
        for bus_info in bus_infos:
            bus_names.add(bus_info.busname)
        print(f"bus_names{bus_names}")
        # 返回公交站名的集合
        return bus_names

    def search_rides(self, search_params):
        # 初始化查询
        passenger_ride_query = PassengerRide.select()
        card_ride_query = CardRide.select()

        # 处理ride_id
        if 'ride_id' in search_params and search_params['ride_id'] != '/':
            passenger_ride_query = passenger_ride_query.where(PassengerRide.ride_id == search_params['ride_id'])
            card_ride_query = card_ride_query.where(CardRide.ride_id == search_params['ride_id'])

            # 处理乘客/卡ID
        if len(search_params['entity_id']) == 18 and search_params['entity_id'] != '/':
            print("zai2")
            passenger_ride_query = passenger_ride_query.where(
                PassengerRide.passenger_id == search_params['entity_id'])
            card_ride_query = None
            print("done")
            print(passenger_ride_query.count())

        if len(search_params['entity_id']) == 9 and search_params['entity_id'] != '/':
            print("zai")
            card_ride_query = card_ride_query.where(CardRide.card_id == search_params['entity_id'])
            passenger_ride_query = None
            print("done")
            print(card_ride_query.count())

        # 处理起始/终止站点
        if 'start_station' in search_params and search_params['start_station'] != '/':
            station_obj = Station.get_or_none(Station.station_name == search_params['start_station'])
            if station_obj and passenger_ride_query is not None:
                passenger_ride_query = passenger_ride_query.where(PassengerRide.start_station == station_obj)
            if station_obj and card_ride_query is not None:
                card_ride_query = card_ride_query.where(CardRide.start_station == station_obj)

        if 'end_station' in search_params and search_params['end_station'] != '/':
            station_obj = Station.get_or_none(Station.station_name == search_params['end_station'])
            if station_obj and passenger_ride_query is not None:
                passenger_ride_query = passenger_ride_query.where(PassengerRide.end_station == station_obj)
            if station_obj and card_ride_query is not None:
                card_ride_query = card_ride_query.where(CardRide.end_station == station_obj)

                # 处理时间段
                # 处理时间段，包括start_time和end_time
                # 处理时间范围
        if ('start_time_from' in search_params and 'start_time_to' in search_params
                and search_params['start_time_from'] != '/' and search_params['end_time_to'] != '/'):
            print(search_params['start_time_from'])
            # start_time_from = datetime.strptime(search_params['start_time_from'], '%Y-%m-%d %H:%M:%S.%f')
            # start_time_to = datetime.strptime(search_params['start_time_to'], '%Y-%m-%d %H:%M:%S.%f')
            # print(start_time_from)

            # 注意：这里假设你的Peewee模型中的日期时间字段是DateTimeField或TimestampField
            if passenger_ride_query is not None:
                passenger_ride_query = passenger_ride_query.where(
                    (PassengerRide.start_time >= search_params['start_time_from']) & (
                            PassengerRide.start_time <= search_params['end_time_to'])
                )
            if card_ride_query is not None:
                card_ride_query = card_ride_query.where(
                    (CardRide.start_time >= search_params['start_time_from']) & (
                            CardRide.start_time <= search_params['end_time_to'])
                )

            # 如果还有end_time，则添加相应的查询条件
        if ('end_time_from' in search_params and 'end_time_to' in search_params
                and search_params['end_time_from'] != '/' and search_params['end_time_to'] != '/'):
            # end_time_from = datetime.strptime(search_params['end_time_from'], '%Y-%m-%d %H:%M:%S.%f')
            # end_time_to = datetime.strptime(search_params['end_time_to'], '%Y-%m-%d %H:%M:%S.%f')
            if passenger_ride_query is not None:
                passenger_ride_query = passenger_ride_query.where(
                    (PassengerRide.end_time >= search_params['end_time_from']) & (
                            PassengerRide.end_time <= search_params['end_time_to'])
                    if PassengerRide.end_time is not None else True
                )

            # 同样地，为CardRide添加查询条件
            if card_ride_query is not None:
                card_ride_query = card_ride_query.where(
                    (CardRide.end_time >= search_params['end_time_from']) & (
                            CardRide.end_time <= search_params['end_time_to'])
                    if CardRide.end_time is not None else True
                )

        # print(passenger_ride_query)
        # # 执行查询并获取结果
        # passenger_rides = list(passenger_ride_query)
        # card_rides = list(card_ride_query)
        # print(passenger_rides)
        passenger_rides_json = {}
        card_rides_json = {}

        # 执行查询并获取结果
        if passenger_ride_query is not None:
            passenger_rides_dicts = list(passenger_ride_query.dicts())
            passenger_rides_json = json.dumps(passenger_rides_dicts, ensure_ascii=False, cls=DecimalDatetimeEncoder)
        if card_ride_query is not None:
            card_rides_dicts = list(card_ride_query.dicts())
            card_rides_json = json.dumps(card_rides_dicts, ensure_ascii=False, cls=DecimalDatetimeEncoder)

        # print(f"result_old{passenger_ride_query}")
        # print(f"result_new{passenger_rides_dicts}")

        # 使用json.dumps()将字典列表转换为JSON字符串

        # print(f"result_fresh{card_rides_json}")

        # 合并结果（如果需要）或分别返回
        return passenger_rides_json, card_rides_json


class DecimalDatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)  # 或者 float(obj) 将 Decimal 转换为浮点数
        elif isinstance(obj, datetime):
            return obj.isoformat()  # 将 datetime 转换为 ISO 8601 格式的字符串
        return super(DecimalDatetimeEncoder, self).default(obj)
