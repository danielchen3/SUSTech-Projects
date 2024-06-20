from peewee import (
    Model, CharField, TimeField, TextField, FloatField, DateField, IntegerField,
    DecimalField, DateTimeField, ForeignKeyField, CompositeKey
)
from playhouse.pool import PooledPostgresqlExtDatabase
from datetime import datetime

from config import Config

db = PooledPostgresqlExtDatabase(
    database=Config.DATABASE_NAME,
    user='postgres',
    password='123456789Bw&',
    host=Config.DATABASE_HOST,
    port=Config.DATABASE_PORT,
    max_connections=100,  # 最大连接数
    stale_timeout=600  # 空闲连接超时
)


class BaseModel(Model):
    class Meta:
        database = db


class Line(BaseModel):
    line_name = CharField(primary_key=True, max_length=255)
    start_time = TimeField()
    end_time = TimeField()
    intro = TextField()
    mileage = FloatField()
    color = CharField(max_length=50)
    first_opening = DateField()
    url = CharField(max_length=255)

    class Meta:
        db_table = 'lines'


class Station(BaseModel):
    station_name = CharField(primary_key=True)  # 假设station_name是唯一的
    district = CharField()
    intro = TextField()
    chinese_name = CharField()

    class Meta:
        db_table = 'station'


class LineStation(BaseModel):
    id = IntegerField(primary_key=True)
    line_name = ForeignKeyField(Line, backref='line_stations', column_name='line_name')
    station_name = ForeignKeyField(Station, backref='line_stations', column_name='station_name')

    class Meta:
        db_table = 'line_stations'


class BusInfo(BaseModel):
    busname = CharField()
    chukou = CharField()
    station = ForeignKeyField(Station, backref='bus_infos', column_name='station_name')
    bus_info = TextField()

    class Meta:
        primary_key = CompositeKey('busname', 'chukou', 'station')
        db_table = 'bus_info'


class OutInfo(BaseModel):
    id = IntegerField(primary_key=True)
    station = ForeignKeyField(Station, backref='out_infos', column_name='station_name')
    outt = CharField()
    textt = CharField()

    class Meta:
        db_table = 'out_info'


class Card(BaseModel):
    code_id = CharField(primary_key=True)
    money = DecimalField(max_digits=10, decimal_places=2)  # 假设我们有一个DecimalField
    create_time = DateTimeField(default=datetime.now)  # 使用DateTimeField而不是timestamp

    class Meta:
        db_table = 'card'

    def get_ongoing_rides(self):
        """获取公交卡当前上车但未下车的乘车记录"""
        current_time = datetime.now()
        return (CardRide
                .select(CardRide, Station)
                .join(Station, on=(CardRide.start_station == Station.station_name))
                .where(CardRide.card == self)
                .where(CardRide.end_time.is_null(True))
                .where(CardRide.start_time <= current_time)
                .order_by(CardRide.start_time.desc()))


class Passenger(BaseModel):
    id_number = CharField(primary_key=True)
    name = CharField()
    phone_number = CharField()
    gender = CharField()
    district = CharField()

    class Meta:
        db_table = 'passenger'


class PassengerRide(BaseModel):
    ride_id = IntegerField(primary_key=True)
    passenger_id = ForeignKeyField(Passenger, backref='passenger_rides', column_name='passenger_id')
    start_station = ForeignKeyField(Station, backref='passenger_start_rides', column_name='start_station')
    end_station = ForeignKeyField(Station, backref='passenger_end_rides', column_name='end_station')
    price = DecimalField(max_digits=10, decimal_places=2)
    start_time = DateTimeField(default=datetime.now)
    end_time = DateTimeField(null=True)

    class Meta:
        db_table = 'passenger_ride'


class CardRide(BaseModel):
    ride_id = IntegerField(primary_key=True)
    card_id = ForeignKeyField(Card, backref='card_rides', column_name='card_id', to_field='code_id')
    start_station = ForeignKeyField(Station, backref='card_start_rides', column_name='start_station')
    end_station = ForeignKeyField(Station, backref='card_end_rides', column_name='end_station')
    price = DecimalField(max_digits=10, decimal_places=2)
    start_time = DateTimeField(default=datetime.now)
    end_time = DateTimeField(null=True)

    class Meta:
        db_table = 'card_ride'


def get_ongoing_passenger_rides():
    """获取乘客当前上车但未下车的乘车记录"""
    current_time = datetime.now()
    ongoing_rides = (PassengerRide
                     .select(PassengerRide, Station)
                     .join(Station, on=(PassengerRide.start_station == Station.station_name))
                     .where(PassengerRide.end_time.is_null(True))
                     .where(PassengerRide.passenger_id.is_null(False))
                     .where(PassengerRide.start_time <= current_time)
                     .order_by(PassengerRide.start_time.desc()))
    result = []
    for ride in ongoing_rides:
        result.append({
            'ride_id': ride.ride_id,
            'passenger_id': ride.passenger_id.id_number,
            'start_station': ride.start_station.station_name,
            'start_time': ride.start_time.strftime('%Y-%m-%d %H:%M:%S')
        })
    return result


def get_ongoing_card_rides():
    """获取乘客当前上车但未下车的乘车记录"""
    current_time = datetime.now()
    ongoing_rides = (CardRide
                     .select(CardRide, Station)
                     .join(Station, on=(CardRide.start_station == Station.station_name))
                     .where(CardRide.end_time.is_null(True))
                     .where(CardRide.card_id.is_null(False))
                     .where(CardRide.start_time <= current_time)
                     .order_by(CardRide.start_time.desc()))
    result = []
    for ride in ongoing_rides:
        result.append({
            'ride_id': ride.ride_id,
            'card_id': ride.card_id.code_id,
            'start_station': ride.start_station.station_name,
            'start_time': ride.start_time.strftime('%Y-%m-%d %H:%M:%S')
        })
    return result

# import pymysql
#
# pymysql.install_as_MySQLdb()
# from peewee import (
#     Model, CharField, TimeField, TextField, FloatField, DateField, IntegerField,
#     DecimalField, DateTimeField, ForeignKeyField, CompositeKey
# )
# from playhouse.pool import PooledMySQLDatabase
# from datetime import datetime
#
# db = PooledMySQLDatabase(
#     database='project1',
#     user='root',  # MySQL 的默认用户
#     password='123456789Bw&',
#     host='localhost',
#     port=3306,  # MySQL 的默认端口
#     max_connections=100,  # 最大连接数
#     stale_timeout=600  # 空闲连接超时
# )
#
#
# class BaseModel(Model):
#     class Meta:
#         database = db
#
#
# class Line(BaseModel):
#     line_name = CharField(primary_key=True, max_length=255)
#     start_time = TimeField()
#     end_time = TimeField()
#     intro = TextField()
#     mileage = FloatField()
#     color = CharField(max_length=50)
#     first_opening = DateField()
#     url = CharField(max_length=255)
#
#     class Meta:
#         db_table = 'lines'
#
#
# class Station(BaseModel):
#     station_name = CharField(primary_key=True)  # 假设station_name是唯一的
#     district = CharField()
#     intro = TextField()
#     chinese_name = CharField()
#
#     class Meta:
#         db_table = 'station'
#
#
# class LineStation(BaseModel):
#     id = IntegerField(primary_key=True)
#     line_name = ForeignKeyField(Line, backref='line_stations', column_name='line_name')
#     station_name = ForeignKeyField(Station, backref='line_stations', column_name='station_name')
#
#     class Meta:
#         db_table = 'line_stations'
#
#
# class BusInfo(BaseModel):
#     bus_name = CharField()
#     chukou = CharField()
#     station = ForeignKeyField(Station, backref='bus_infos', column_name='station_name')
#     bus_info = TextField()
#
#     class Meta:
#         primary_key = CompositeKey('bus_name', 'chukou', 'station')
#         db_table = 'bus_info'
#
#
# class OutInfo(BaseModel):
#     id = IntegerField(primary_key=True)
#     station = ForeignKeyField(Station, backref='out_infos', column_name='station_name')
#     outt = CharField()
#     textt = CharField()
#
#     class Meta:
#         db_table = 'out_info'
#
#
# class Card(BaseModel):
#     code_id = CharField(primary_key=True)
#     money = DecimalField(max_digits=10, decimal_places=2)  # 假设我们有一个DecimalField
#     create_time = DateTimeField(default=datetime.now)  # 使用DateTimeField而不是timestamp
#
#     class Meta:
#         db_table = 'card'
#
#     def get_ongoing_rides(self):
#         """获取公交卡当前上车但未下车的乘车记录"""
#         current_time = datetime.now()
#         return (CardRide
#                 .select(CardRide, Station)
#                 .join(Station, on=(CardRide.start_station == Station.station_name))
#                 .where(CardRide.card == self)
#                 .where(CardRide.end_time.is_null(True))
#                 .where(CardRide.start_time <= current_time)
#                 .order_by(CardRide.start_time.desc()))
#
#
# class Passenger(BaseModel):
#     id_number = CharField(primary_key=True)
#     name = CharField()
#     phone_number = CharField()
#     gender = CharField()
#     district = CharField()
#
#     class Meta:
#         db_table = 'passenger'
#
#
# class PassengerRide(BaseModel):
#     ride_id = IntegerField(primary_key=True)
#     passenger_id = ForeignKeyField(Passenger, backref='passenger_rides', column_name='passenger_id')
#     start_station = ForeignKeyField(Station, backref='passenger_start_rides', column_name='start_station')
#     end_station = ForeignKeyField(Station, backref='passenger_end_rides', column_name='end_station')
#     price = DecimalField(max_digits=10, decimal_places=2)
#     start_time = DateTimeField(default=datetime.now)
#     end_time = DateTimeField(null=True)
#
#     class Meta:
#         db_table = 'passenger_ride'
#
#
# class CardRide(BaseModel):
#     ride_id = IntegerField(primary_key=True)
#     card_id = ForeignKeyField(Card, backref='card_rides', column_name='card_id', to_field='code_id')
#     start_station = ForeignKeyField(Station, backref='card_start_rides', column_name='start_station')
#     end_station = ForeignKeyField(Station, backref='card_end_rides', column_name='end_station')
#     price = DecimalField(max_digits=10, decimal_places=2)
#     start_time = DateTimeField(default=datetime.now)
#     end_time = DateTimeField(null=True)
#
#     class Meta:
#         db_table = 'card_ride'
#
#
# def get_ongoing_passenger_rides():
#     """获取乘客当前上车但未下车的乘车记录"""
#     current_time = datetime.now()
#     ongoing_rides = (PassengerRide
#                      .select(PassengerRide, Station)
#                      .join(Station, on=(PassengerRide.start_station == Station.station_name))
#                      .where(PassengerRide.end_time.is_null(True))
#                      .where(PassengerRide.passenger_id.is_null(False))
#                      .where(PassengerRide.start_time <= current_time)
#                      .order_by(PassengerRide.start_time.desc()))
#     result = []
#     for ride in ongoing_rides:
#         result.append({
#             'ride_id': ride.ride_id,
#             'passenger_id': ride.passenger_id.id_number,
#             'start_station': ride.start_station.station_name,
#             'start_time': ride.start_time.strftime('%Y-%m-%d %H:%M:%S')
#         })
#     return result
#
#
# def get_ongoing_card_rides():
#     """获取乘客当前上车但未下车的乘车记录"""
#     current_time = datetime.now()
#     ongoing_rides = (CardRide
#                      .select(CardRide, Station)
#                      .join(Station, on=(CardRide.start_station == Station.station_name))
#                      .where(CardRide.end_time.is_null(True))
#                      .where(CardRide.card_id.is_null(False))
#                      .where(CardRide.start_time <= current_time)
#                      .order_by(CardRide.start_time.desc()))
#     result = []
#     for ride in ongoing_rides:
#         result.append({
#             'ride_id': ride.ride_id,
#             'card_id': ride.card_id.code_id,
#             'start_station': ride.start_station.station_name,
#             'start_time': ride.start_time.strftime('%Y-%m-%d %H:%M:%S')
#         })
#     return result
