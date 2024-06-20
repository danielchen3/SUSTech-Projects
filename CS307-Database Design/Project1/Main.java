import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.alibaba.fastjson.parser.Feature;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.List;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.*;
import java.util.Arrays;
import java.util.List;

public class Main {
    private static final String JDBC_URL = "jdbc:postgresql://localhost:5432/cs308";
    private static final String USER = "checker";
    private static final String PASSWORD = "123456";
    private static final String INSERT_CARD_RIDE_SQL = "INSERT INTO card_ride (card_id, start_station, end_station, price, start_time, end_time) VALUES (?, ?, ?, ?, ?, ?)";
    private static final String INSERT_PASSENGER_RIDE_SQL = "INSERT INTO passenger_ride (passenger_id, start_station, end_station, price, start_time, end_time) VALUES (?,?, ?, ?, ?, ?)";

    public static void main(String[] args) throws IOException {

        List<Cards> cards = readJsonArray(Path.of("C:\\Users\\zxt\\Documents\\WeChat Files\\wxid_3pnct7oy24yu22\\FileStorage\\File\\2024-04\\cards(1).json"), Cards.class);
        List<Ride> rides = readJsonArray(Path.of("C:\\Users\\zxt\\Documents\\WeChat Files\\wxid_3pnct7oy24yu22\\FileStorage\\File\\2024-04\\ride(1).json"), Ride.class);
        List<Passenger> pas = readJsonArray(Path.of("C:\\Users\\zxt\\Documents\\WeChat Files\\wxid_3pnct7oy24yu22\\FileStorage\\File\\2024-04\\passenger(1).json"), Passenger.class);
////
//
////
////（这一段可以通过修改导入station,out_info,bus_info）
        try (Connection conn = DriverManager.getConnection(JDBC_URL, USER, PASSWORD)) {
            int j=1;
            conn.setAutoCommit(false); // 开启事务处理
            String jsonStrings = Files.readString(Path.of("C:\\Users\\zxt\\Documents\\WeChat Files\\wxid_3pnct7oy24yu22\\FileStorage\\File\\2024-04\\stations(1).json"));
            JSONObject jsonObject = JSONObject.parseObject(jsonStrings, Feature.OrderedField);
            String insertSql = "INSERT INTO out_info (id,station_name,outt,textt) VALUES (?,?, ?, ?)";
            PreparedStatement pstmt = conn.prepareStatement(insertSql);

            for (String stationName : jsonObject.keySet()) {
                JSONObject station = jsonObject.getJSONObject(stationName);
                String district = station.getString("district");
                String chineseName = station.getString("chinese_name");
                String intro = station.getString("intro");




//                System.out.println("----------Station Name:" + stationName+"----------");
//                System.out.println("District: " + district);
//                System.out.println("Chinese Name: " + chineseName);
//                System.out.println("Introduction: " + intro);
//                System.out.println("--BusInfo");
                JSONArray busInfoArray = JSONArray.parseArray(station.getString("bus_info"));

                for (Object busInfoObject : busInfoArray) {
                    JSONObject busInfo = (JSONObject) busInfoObject;
                    System.out.println("\tchukou: " + busInfo.getString("chukou"));
                    JSONArray busOutInfoArray = busInfo.getJSONArray("busOutInfo");
                    for (Object busOutObject : busOutInfoArray) {
                        JSONObject busOutInfo = (JSONObject) busOutObject;
                        String[] buslines = busOutInfo.getString("busInfo").split("、");
                        System.out.println("\tbusInfo: " + Arrays.toString(buslines));
                        System.out.println("\tbusName: " + busOutInfo.getString("busName"));
                        if(!busOutInfo.getString("busName").equals("")){

                        }
                    }
                }


                System.out.println("--TexttInfo");
                JSONArray outInfoArray = JSONArray.parseArray(station.getString("out_info"));

                for (Object outInfoObject : outInfoArray) {
                    JSONObject outInfo = (JSONObject) outInfoObject;
                    System.out.println("\toutt: " + outInfo.getString("outt").trim());
                    String[] textt = outInfo.getString("textt").split("、");
                    System.out.println("\ttextt: " + Arrays.toString(textt));
                    pstmt.setInt(1, j);
                    j++;
                    pstmt.setString(2, stationName);
                    pstmt.setString(3,  outInfo.getString("outt").trim());
                    pstmt.setString(4, Arrays.toString(textt));
                    pstmt.addBatch();

                }
            }
            int[] affectedRows = pstmt.executeBatch(); // 执行批处理

// 执行你的 SQL 语句

            conn.commit(); // 提交事务
        }
        catch (SQLException e) {
            e.printStackTrace();
        }






        long starTime = System.currentTimeMillis();
        //这一段可以通过修改导入bus_ride 和passenger_ride
        try (Connection conn = DriverManager.getConnection(JDBC_URL, USER, PASSWORD)) {
            conn.setAutoCommit(false); // 开启事务处理


            String insertSql = "INSERT INTO passenger_ride (ride_id,passenger_id, start_station, end_station,price,start_time,end_time) VALUES (?,?, ?, ?, ?, ?, ?)";
            PreparedStatement pstmt = conn.prepareStatement(insertSql);
            int j=1;

            for (Ride ride : rides) {
                if(ride.getUser().length()>10){
                    pstmt.setInt(1, j);
                    j++;
                    pstmt.setString(2, ride.getUser());
                    pstmt.setString(3, ride.getStartStation());
                    pstmt.setString(4, ride.getEndStation());
                    pstmt.setDouble(5, ride.getPrice());
                    java.time.LocalDateTime createTime = ride.getStartTime();
                    java.sql.Timestamp sqlTimestamp = Timestamp.valueOf(createTime);
                    pstmt.setTimestamp(6, sqlTimestamp);
                    java.time.LocalDateTime endTimee = ride.getEndTime();
                    java.sql.Timestamp sqlendstampe = Timestamp.valueOf(endTimee);
                    pstmt.setTimestamp(7, sqlendstampe);
                    pstmt.addBatch();
                }
                else{

                }

                // 设置PreparedStatement的参数，根据Cards类的属性和数据库表的字段进行调整

                // ... 设置其他属性


                 // 添加到批处理
            }

            int[] affectedRows = pstmt.executeBatch(); // 执行批处理
            conn.commit(); // 提交事务

            System.out.println("pass imported successfully.");
        } catch (SQLException e) {
            e.printStackTrace();
        }
        long enTime = System.currentTimeMillis();
        long totalTime = enTime - starTime;
        System.out.println("程序运行时间: " + totalTime + " 毫秒");






        importCardsToDatabase(cards);//这一段导入cards
        importpassToDatabase(pas);//这一段导入passenger


//        try {
//            importCardRidesToDatabase(rides);
//            importPassengerRidesToDatabase(rides);
//            System.out.println("Imports completed successfully.");
//        } catch (SQLException e) {
//            e.printStackTrace();
//        }无用
////导入line_station以及lines
        try (Connection conn = DriverManager.getConnection(JDBC_URL, USER, PASSWORD)) {

            conn.setAutoCommit(false); // 开启事务处理
            String insertSql = "INSERT INTO line_stations (id,line_name, station_name) VALUES (?, ?, ?)";
            String jsonStrings = Files.readString(Path.of("C:\\Users\\zxt\\Documents\\WeChat Files\\wxid_3pnct7oy24yu22\\FileStorage\\File\\2024-04\\lines(1).json"));
            JSONObject jsonObject = JSONObject.parseObject(jsonStrings, Feature.OrderedField);
            int j=1;
            PreparedStatement pstmt = conn.prepareStatement(insertSql);
            for (String line_name : jsonObject.keySet()) {
                JSONObject station = jsonObject.getJSONObject(line_name);
                String startt = station.getString("start_time");
                String endt = station.getString("end_time");
                DateTimeFormatter formatter = DateTimeFormatter.ofPattern("HH:mm");
                LocalTime startTime = LocalTime.parse(startt, formatter);
                LocalTime endTime = LocalTime.parse(endt, formatter);
                String intro = station.getString("intro");
                String color = station.getString("color");
                String url = station.getString("url");
                String mil = station.getString("mileage");
                double mileage = Double.parseDouble(mil);
                String dat = station.getString("first_opening");
                DateTimeFormatter inputFormatter = DateTimeFormatter.ofPattern("yyyy-M-dd");
                DateTimeFormatter outputFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
                LocalDate firstOpening = null;
                String[] stationsArray = station.getString("stations").split(",");
                for (String stationName : stationsArray) {
                    // 去除字符串两端的空白字符（如果有的话）
                    stationName = stationName.replaceAll("[,\"\\[\\]]", "");
                    stationName = stationName.replaceFirst("\\n$", "");
                    if (stationName.equals("Huilongpu  station\n")) {
                        stationName = "Huilongpu  station";

                    }

                    // 去除双引号、逗号和方括号
                    System.out.println(stationName);

                    pstmt.setInt(1, j);
                    j++;
                    pstmt.setString(2, line_name);
                    pstmt.setString(3, stationName);
                    pstmt.addBatch(); // 添加到批处理

                    // 打印站名或进行其他操作

                }


                try {
                    // 解析输入日期字符串为LocalDate对象
                    LocalDate date = LocalDate.parse(dat, inputFormatter);

                    // 将LocalDate对象格式化为标准的输出字符串
                    String outputDateString = date.format(outputFormatter);
                    firstOpening = LocalDate.parse(outputDateString);

                    // 输出转换后的日期字符串
                } catch (java.time.format.DateTimeParseException e) {
                    // 处理解析异常
                    e.printStackTrace();
                }

                pstmt.setString(1, line_name);
                pstmt.setTime(2, Time.valueOf(startTime));
                pstmt.setTime(3, Time.valueOf(endTime));
                pstmt.setString(4, intro);
                pstmt.setDouble(5, mileage);
                pstmt.setString(6, color);
                pstmt.setDate(7, Date.valueOf(firstOpening));
                pstmt.setString(8, url);
                pstmt.addBatch(); // 添加到批处理


//
//
//
////
            }
            int[] affectedRows = pstmt.executeBatch(); // 执行批处理
            conn.commit(); // 提交事务

            System.out.println("st imported successfully.");
        }
            catch (SQLException e) {
            e.printStackTrace();
        }









    }
//导入cards
    private static void importCardsToDatabase(List<Cards> cards) {
        try (Connection conn = DriverManager.getConnection(JDBC_URL, USER, PASSWORD)) {
            conn.setAutoCommit(false); // 开启事务处理

            String insertSql = "INSERT INTO card (code_id, money, create_time) VALUES (?, ?, ?)";
            PreparedStatement pstmt = conn.prepareStatement(insertSql);

            for (Cards card : cards) {
                // 设置PreparedStatement的参数，根据Cards类的属性和数据库表的字段进行调整
                pstmt.setString(1, card.getCode());
                pstmt.setDouble(2, card.getMoney());
                java.time.LocalDateTime createTime = card.getCreate_time();
                java.sql.Timestamp sqlTimestamp = Timestamp.valueOf(createTime);
                pstmt.setTimestamp(3, sqlTimestamp);
                // ... 设置其他属性

                pstmt.addBatch(); // 添加到批处理
            }

            int[] affectedRows = pstmt.executeBatch(); // 执行批处理
            conn.commit(); // 提交事务

            System.out.println("Cards imported successfully.");
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
    //导入passengers
    private static void importpassToDatabase(List<Passenger> pas) {
        try (Connection conn = DriverManager.getConnection(JDBC_URL, USER, PASSWORD)) {
            conn.setAutoCommit(false); // 开启事务处理

            String insertSql = "INSERT INTO passenger (id_number, name, phone_number,gender,district) VALUES (?, ?, ?, ?, ?)";
            PreparedStatement pstmt = conn.prepareStatement(insertSql);

            for (Passenger pa : pas) {
                // 设置PreparedStatement的参数，根据Cards类的属性和数据库表的字段进行调整
                pstmt.setString(1, pa.getIdNumber());
                pstmt.setString(2, pa.getName());
                pstmt.setString(3, pa.getPhoneNumber());
                pstmt.setString(4, pa.getGender());
                pstmt.setString(5, pa.getDistrict());
                // ... 设置其他属性

                pstmt.addBatch(); // 添加到批处理
            }

            int[] affectedRows = pstmt.executeBatch(); // 执行批处理
            conn.commit(); // 提交事务

            System.out.println("pass imported successfully.");
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
//
    private static <T> List<T> readJsonArray(Path path, Class<T> clz) {
        try {
            String jsonStrings = Files.readString(path);
            return JSON.parseArray(jsonStrings, clz);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }


}







//