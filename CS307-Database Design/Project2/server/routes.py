import logging
from datetime import datetime

from flask import request, jsonify, current_app as app, Flask, session
from playhouse.shortcuts import model_to_dict

from models import Line, Passenger, CardRide, Station, PassengerRide, get_ongoing_passenger_rides, \
    get_ongoing_card_rides
from db_handler import DatabaseHandler
from exceptions import NotFoundException

db_credentials = {}

# Configure logging
logging.basicConfig(level=logging.DEBUG)


class AlreadyExist(Exception):
    pass


def create_routes(app):
    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        username = data.get('username')
        password = data.get('password')
        print("在Login route")
        try:
            db_handler = DatabaseHandler(username, password)
            # session['username'] = username
            # session['password'] = password
            db_credentials['username'] = username
            db_credentials['password'] = password
            db_handler.close_connection()

            return jsonify({'message': 'Login successful'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 401

    @app.route('/find_line/<line_name>', methods=['GET'])
    def find_line(line_name):
        username = db_credentials.get('username')
        password = db_credentials.get('password')

        if not username or not password:
            return jsonify({'error': 'Unauthorized'}), 401

        db_handler = DatabaseHandler(username, password)
        print(f"在route.py里面的{line_name}")
        try:
            result = db_handler.find_line(line_name)
            print(result)
            db_handler.close_connection()
            return jsonify({'result': result}), 200
        except NotFoundException as e:
            db_handler.close_connection()
            return jsonify({'error': str(e)}), 404

    @app.route('/add_line', methods=['POST'])
    def add_line():
        username = db_credentials.get('username')
        password = db_credentials.get('password')

        if not username or not password:
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.json
        print(data)

        required_fields = ['line_name', 'start_time', 'end_time', 'intro', 'mileage', 'color', 'first_opening', 'url']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing fields'}), 400

        db_handler = DatabaseHandler(username, password)
        try:
            result = db_handler.add_line(data)
            db_handler.close_connection()
            return jsonify({'message': result}), 200
        except AlreadyExist as e:
            db_handler.close_connection()
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            db_handler.close_connection()
            return jsonify({'error': str(e)}), 500

    # @app.route('/add_line', methods=['POST'])
    # def add_line():
    #     username = db_credentials.get('username')
    #     password = db_credentials.get('password')
    # 
    #     if not username or not password:
    #         return jsonify({'error': 'Unauthorized'}), 401
    # 
    #     data = request.json
    #     line_name = data.get('line_name')
    #     start_time = data.get('start_time')
    #     end_time = data.get('end_time')
    #     intro = data.get('intro')
    #     mileage = data.get('mileage')
    #     color = data.get('color')
    #     first_opening = data.get('first_opening')
    #     url = data.get('url')
    # 
    #     if not all([line_name, start_time, end_time, intro, mileage, color, first_opening, url]):
    #         return jsonify({'error': 'Missing fields'}), 400
    # 
    #     db_handler = DatabaseHandler(username, password)
    #     try:
    #         Line.create(
    #             line_name=line_name,
    #             start_time=start_time,
    #             end_time=end_time,
    #             intro=intro,
    #             mileage=mileage,
    #             color=color,
    #             first_opening=first_opening,
    #             url=url
    #         )
    #         db_handler.close_connection()
    #         return jsonify({'message': 'Line added successfully'}), 200
    #     except Exception as e:
    #         db_handler.close_connection()
    #         return jsonify({'error': str(e)}), 500

    @app.route('/delete_line/<line_name>', methods=['DELETE'])
    def delete_line(line_name):
        username = db_credentials.get('username')
        password = db_credentials.get('password')
        print(f"在route.py里{line_name}")
        if not username or not password:
            return jsonify({'error': 'Unauthorized'}), 401

        db_handler = DatabaseHandler(username, password)
        try:
            result = db_handler.delete_line(line_name)
            print("Delete Successfully!")
            db_handler.close_connection()
            return jsonify({'message': result}), 200
        except NotFoundException as e:
            db_handler.close_connection()
            return jsonify({'error': str(e)}), 404

    @app.route('/modify_line/', methods=['POST'])
    def modify_line():
        username = db_credentials.get('username')
        password = db_credentials.get('password')
        if not username or not password:
            return jsonify({'error': 'Unauthorized'}), 401

        db_handler = DatabaseHandler(username, password)

        data = request.json
        print(data)

        required_fields = ['line_name', 'start_time', 'end_time', 'intro', 'mileage', 'color', 'first_opening', 'url']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing fields'}), 400

        try:
            result = db_handler.modify_line(data)
            db_handler.close_connection()
            return jsonify({'message': result}), 200
        except NotFoundException as e:
            db_handler.close_connection()
            return jsonify({'error': str(e)}), 404

    @app.route('/add_station', methods=['POST'])
    def add_station():
        username = db_credentials.get('username')
        password = db_credentials.get('password')

        if not username or not password:
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.json
        print(data)

        required_fields = ['station_name', 'district', 'intro', 'chinese_name']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing fields'}), 400

        db_handler = DatabaseHandler(username, password)
        try:
            result = db_handler.add_station(data)
            db_handler.close_connection()
            return jsonify({'message': result}), 200
        except AlreadyExist as e:
            db_handler.close_connection()
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            db_handler.close_connection()
            return jsonify({'error': str(e)}), 500

    @app.route('/delete_station/<station_name>', methods=['DELETE'])
    def delete_station(station_name):
        username = db_credentials.get('username')
        password = db_credentials.get('password')
        # print(f"在route.py里{line_name}")
        if not username or not password:
            return jsonify({'error': 'Unauthorized'}), 401

        db_handler = DatabaseHandler(username, password)
        try:
            result = db_handler.delete_station(station_name)
            print("Delete station Successfully!")
            db_handler.close_connection()
            return jsonify({'message': result}), 200
        except NotFoundException as e:
            db_handler.close_connection()
            return jsonify({'error': str(e)}), 404

    @app.route('/modify_station/', methods=['POST'])
    def modify_station():
        username = db_credentials.get('username')
        password = db_credentials.get('password')
        if not username or not password:
            return jsonify({'error': 'Unauthorized'}), 401

        db_handler = DatabaseHandler(username, password)

        data = request.json

        required_fields = ['station_name', 'district', 'intro', 'chinese_name']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing fields'}), 400

        try:
            result = db_handler.modify_station(data)
            db_handler.close_connection()
            return jsonify({'message': result}), 200
        except NotFoundException as e:
            db_handler.close_connection()
            return jsonify({'error': str(e)}), 404

    @app.route('/insert_station_before', methods=['POST'])
    def insert_station_before():
        username = db_credentials.get('username')
        password = db_credentials.get('password')
        # print(f"在route.py里{line_name}")
        if not username or not password:
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.json
        print(data)

        required_fields = ['line_name', 'before_station_name', 'station_name']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing fields'}), 400

        db_handler = DatabaseHandler(username, password)
        try:
            result = db_handler.insert_station_before(data['line_name'], data['before_station_name'],
                                                      data['station_name'])
            # print(f"result: {result}")
            # print(result['message'])
            if result is not None:
                if result['message'] == 'No Station':
                    print("data fail to insert!")
                    db_handler.close_connection()
                    return jsonify({'message': result}), 404
            db_handler.close_connection()
            return jsonify({'message': result}), 200
        except NotFoundException as e:
            db_handler.close_connection()
            return jsonify({'error': str(e)}), 404

    @app.route('/insert_mul_station_before', methods=['POST'])
    def insert_mul_station_before():
        username = db_credentials.get('username')
        password = db_credentials.get('password')
        # print(f"在route.py里{line_name}")
        if not username or not password:
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.json
        print(data)

        iterable = 1

        if data['line_name2'] != '/':
            iterable = 2
        if data['line_name3'] != '/':
            iterable = 3

        print(f"iter{iterable}")

        db_handler = DatabaseHandler(username, password)
        if iterable == 1:
            try:
                result = db_handler.insert_station_before(data['line_name1'], data['before_station_name1'],
                                                          data['station_name1'])
                # print(f"result: {result}")
                # print(result['message'])
                if result is not None:
                    if result['message'] == 'No Station':
                        print("data fail to insert!")
                        db_handler.close_connection()
                        return jsonify({'message': result}), 404
                db_handler.close_connection()
                return jsonify({'message': result}), 200
            except NotFoundException as e:
                db_handler.close_connection()
                return jsonify({'error': str(e)}), 404
        elif iterable == 2:
            try:
                result1 = db_handler.insert_station_before(data['line_name1'], data['before_station_name1'],
                                                          data['station_name1'])

                result2 = db_handler.insert_station_before(data['line_name2'], data['before_station_name2'],
                                                          data['station_name2'])
                # print(f"result: {result}")
                # print(result['message'])
                if result1 is not None:
                    if result1['message'] == 'No Station':
                        print("data fail to insert!")
                        db_handler.close_connection()
                        return jsonify({'message': result1}), 404
                elif result2 is not None:
                    if result2['message'] == 'No Station':
                        print("data fail to insert!")
                        db_handler.close_connection()
                        return jsonify({'message': result2}), 404
                db_handler.close_connection()
                return jsonify({'message': result1}), 200
            except NotFoundException as e:
                db_handler.close_connection()
                return jsonify({'error': str(e)}), 404

        elif iterable == 3:
            try:
                result1 = db_handler.insert_station_before(data['line_name1'], data['before_station_name1'],
                                                          data['station_name1'])

                result2 = db_handler.insert_station_before(data['line_name2'], data['before_station_name2'],
                                                          data['station_name2'])

                result3 = db_handler.insert_station_before(data['line_name3'], data['before_station_name3'],
                                                           data['station_name3'])
                # print(f"result: {result}")
                # print(result['message'])
                if result1 is not None:
                    if result1['message'] == 'No Station':
                        print("data fail to insert!")
                        db_handler.close_connection()
                        return jsonify({'message': result1}), 404
                if result2 is not None:
                    if result2['message'] == 'No Station':
                        print("data fail to insert!")
                        db_handler.close_connection()
                        return jsonify({'message': result2}), 404
                if result3 is not None:
                    if result3['message'] == 'No Station':
                        print("data fail to insert!")
                        db_handler.close_connection()
                        return jsonify({'message': result3}), 404
                db_handler.close_connection()
                return jsonify({'message': result1}), 200
            except NotFoundException as e:
                db_handler.close_connection()
                return jsonify({'error': str(e)}), 404


    @app.route('/remove_station_from_line', methods=['DELETE'])
    def remove_station_from_line():
        username = db_credentials.get('username')
        password = db_credentials.get('password')
        # print(f"在route.py里{line_name}")
        if not username or not password:
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.json
        print(data)
        print("data:")

        required_fields = ['line_name', 'station_name']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing fields'}), 400

        db_handler = DatabaseHandler(username, password)
        try:
            result = db_handler.remove_station_from_line(data['line_name'], data['station_name'])
            print("data deleted successfully!")
            db_handler.close_connection()
            return jsonify({'message': result}), 200
        except NotFoundException as e:
            db_handler.close_connection()
            return jsonify({'error': str(e)}), 404

    @app.route('/find_n_stations', methods=['POST'])
    def find_n_stations():
        username = db_credentials.get('username')
        password = db_credentials.get('password')
        if not username or not password:
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.json
        print(data)

        required_fields = ['line_name', 'station_name', 'is_forward', 'n']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing fields'}), 400

        db_handler = DatabaseHandler(username, password)
        try:
            result = db_handler.find_n_stations(data['line_name'], data['station_name'],
                                                data['is_forward'], data['n'])
            print("Data found successfully!")
            db_handler.close_connection()
            print(f"result: {result}, type: {type(result)}")

            # 确保 result 是可序列化的类型
            if isinstance(result, (list, dict, str, int, float, bool, type(None))):
                return jsonify({'result': result}), 200
            else:
                # 假设 result 是一个模型对象，我们将其转换为字典
                result_dict = model_to_dict(result)
                return jsonify({'result': result_dict}), 200
        except NotFoundException as e:
            db_handler.close_connection()
            return jsonify({'error': str(e)}), 404

    @app.route('/passenger_board', methods=['POST'])
    def passenger_board():
        username = db_credentials.get('username')
        password = db_credentials.get('password')
        # print(f"在route.py里{line_name}")
        if not username or not password:
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.json
        print(data)

        required_fields = ['entity_id', 'start_station_name']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing fields'}), 400

        db_handler = DatabaseHandler(username, password)
        try:
            db_handler.passenger_board(data['entity_id'], data['start_station_name'])
            print("On board Successfully!")
            db_handler.close_connection()
            return jsonify({'message': "Success"}), 200
        except NotFoundException as e:
            db_handler.close_connection()
            return jsonify({'error': str(e)}), 404

    @app.route('/passenger_alight', methods=['POST'])
    def passenger_alight():
        username = db_credentials.get('username')
        password = db_credentials.get('password')
        # print(f"在route.py里{line_name}")
        if not username or not password:
            return jsonify({'error': 'Unauthorized'}), 401

        print("request: ", request)
        data = request.json
        print(data)

        required_fields = ['entity_id', 'end_station_name']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing fields'}), 400

        db_handler = DatabaseHandler(username, password)
        try:
            result = db_handler.passenger_alight(data['entity_id'], data['end_station_name'])
            db_handler.close_connection()
            print(f"result{result}")
            if result['Status'] == 'True':
                print("Off board Successfully!")
                return jsonify({'message': result}), 200
            else:
                return jsonify({'message': result}), 404
        except NotFoundException as e:
            db_handler.close_connection()
            return jsonify({'error': str(e)}), 404

    @app.route('/find_passenger_now', methods=['GET'])
    def find_passenger_now():
        username = db_credentials.get('username')
        password = db_credentials.get('password')
        if not username or not password:
            return jsonify({'error': 'Unauthorized'}), 401

        db_handler = DatabaseHandler(username, password)
        try:
            result = get_ongoing_passenger_rides()
            db_handler.close_connection()
            if result is None or len(result) == 0:
                return jsonify({'error': "Not Found!"}), 404
            return jsonify({'ongoing_rides': result}), 200
        except NotFoundException as e:
            db_handler.close_connection()
            return jsonify({'error': str(e)}), 404

    @app.route('/find_card_now', methods=['GET'])
    def find_card_now():
        username = db_credentials.get('username')
        password = db_credentials.get('password')
        if not username or not password:
            return jsonify({'error': 'Unauthorized'}), 401

        db_handler = DatabaseHandler(username, password)
        try:
            result = get_ongoing_card_rides()
            db_handler.close_connection()
            if result is None or len(result) == 0:
                return jsonify({'error': "Not Found!"}), 404
            return jsonify({'ongoing_rides': result}), 200
        except NotFoundException as e:
            db_handler.close_connection()
            return jsonify({'error': str(e)}), 404

    @app.route('/find_path', methods=['GET'])
    def find_path():
        username = db_credentials.get('username')
        password = db_credentials.get('password')
        if not username or not password:
            return jsonify({'error': 'Unauthorized'}), 401

        print("request: ", request)
        data = request.json
        print(data)

        required_fields = ['start_station', 'end_station']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing fields'}), 400

        db_handler = DatabaseHandler(username, password)
        try:
            result = db_handler.find_path(data['start_station'], data['end_station'])
            db_handler.close_connection()
            if result is None or len(result) == 0:
                return jsonify({'error': "Not Found!"}), 404
            return jsonify({'result': result}), 200
        except NotFoundException as e:
            db_handler.close_connection()
            return jsonify({'error': str(e)}), 404

    @app.route('/find_stations_by_bus_line', methods=['GET'])
    def find_stations_by_bus_line():
        username = db_credentials.get('username')
        password = db_credentials.get('password')
        if not username or not password:
            return jsonify({'error': 'Unauthorized'}), 401

        print("request: ", request)
        data = request.json
        print(data)

        required_fields = ['bus_line']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing fields'}), 400

        db_handler = DatabaseHandler(username, password)
        try:
            result = db_handler.find_stations_by_bus_line(data['bus_line'])
            db_handler.close_connection()
            if result is None or len(result) == 0:
                return jsonify({'error:': "Not Found!"}), 404
            result_list = list(result)
            print(result_list)
            return jsonify({'result': result_list}), 200
        except NotFoundException as e:
            db_handler.close_connection()
            return jsonify({'error': str(e)}), 404

    @app.route('/find_nearby_stations_by_metro_station', methods=['GET'])
    def find_nearby_stations_by_metro_station():
        username = db_credentials.get('username')
        password = db_credentials.get('password')
        if not username or not password:
            return jsonify({'error': 'Unauthorized'}), 401

        print("request: ", request)
        data = request.json
        print(data)

        required_fields = ['station_name']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing fields'}), 400

        db_handler = DatabaseHandler(username, password)
        try:
            result = db_handler.find_nearby_stations_by_metro_station(data['station_name'])
            db_handler.close_connection()
            if result is None or len(result) == 0:
                return jsonify({'error:': "Not Found!"}), 404
            result_list = list(result)
            print(result_list)
            return jsonify({'result': result_list}), 200
        except NotFoundException as e:
            db_handler.close_connection()
            return jsonify({'error': str(e)}), 404

    @app.route('/search_rides', methods=['GET'])
    def search_rides():
        username = db_credentials.get('username')
        password = db_credentials.get('password')
        if not username or not password:
            return jsonify({'error': 'Unauthorized'}), 401

        print("request: ", request)
        data = request.json
        print(data)

        db_handler = DatabaseHandler(username, password)
        try:
            passenger_rides, card_rides = db_handler.search_rides(data)
            db_handler.close_connection()
            # if result is None or len(result) == 0:
            #     return jsonify({'error:': "Not Found!"}), 404
            # print(result_list)
            # print(f"res1{passenger_rides}")
            # passenger_rides_real = list(passenger_rides)
            # card_rides_real = list(card_rides)
            return jsonify({'passenger_rides': passenger_rides, 'card_rides': card_rides}), 200
        except NotFoundException as e:
            db_handler.close_connection()
            return jsonify({'error': str(e)}), 404

    return app
