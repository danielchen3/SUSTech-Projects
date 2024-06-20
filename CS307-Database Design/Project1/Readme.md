# CS307 数据库原理 Project1

## 成员信息与分工

1. 小组成员：陈长信（12210731）、赵欣瞳（12212727）
2. 实验课：Thursday 3-4
3. 任务分配占比   **成员贡献比：陈长信（50%）赵欣瞳（50%）**

|                  Task                  | Author(Name) |
| :------------------------------------: | :----------: |
|               E-R图制作                |    赵欣瞳    |
|              数据库的设计              |    陈长信    |
|           使用Python导入数据           |    陈长信    |
|            使用Java导入数据            |    赵欣瞳    |
|      .sql语句书写与数据准确性检查      |    赵欣瞳    |
|    使用MySQL导入数据与导入速度分析     |    陈长信    |
|    基于Python的多种导入方式速度分析    |    陈长信    |
| 数据集的扩展与不同数据集导入速度的分析 |    赵欣瞳    |

## E-R图

![41b62aa6f8e9cd709490333e7bd0c3b](C:\Users\B_W_Y_Y\Documents\WeChat Files\wxid_jtoqoioxa40q22\FileStorage\Temp\41b62aa6f8e9cd709490333e7bd0c3b.jpg)

**简单描述**

ER图使用`processon.com`生成。实体lines和实体station通过关系line_station连接，一条line可以对应多个stations。station通过station_out与out_info连接，一个地铁站外可以有不同的出口，每个出口外都有不同的建筑。station 通过station_bus与bus_info连接，一个地铁站可以有多个出口，每个出口外都可能有公交站和公交线路。station通过car_ride与card连接，一个car_ride由起始站和终点站决定，一个station可能出现在多个ride中，station与passenger同理。另外，在关系ride中，还有属性记录了ride的始末站与价格。每个实体的主键都已在E-R diagram 中标出，有的是复合主键。

## 数据库设计

![image-20240428003926311](C:\Users\B_W_Y_Y\AppData\Roaming\Typora\typora-user-images\image-20240428003926311.png)

### 简要介绍

**Table Name: lines**

1. **Columns: ** line_name(pk), start_time, end_time, intro, mileage, color, first_opening, url
2. **Description:** 这个表存储所有地铁线路的信息，line_name是lines表的主键，代表线路的名称；无外键；其他的列为描述对应主键的量。

**Table Name: station**

1. **Columns: ** station_name(pk), district, intro, chinese_name
2. **Description:** 这个表存储所有地铁站的信息，station_name是表的主键，代表站的名称；无外键；剩余的列表示对当前station_name的其他描述。

**Table Name: line_stations**

1. **Columns: ** id(pk), line_name(fk), station_name(fk)
2. **Description:** 这个表存储每个地铁线路的途径车站，id是生成的从1开始的自增量作为主键，line_name和station_name作为外键分别指向lines和station表中的主键。

**Table Name: bus_info**

1. **Columns: ** (busName, chukou, station_name)(pk), station_name(fk), bus_info
2. **Description:** 这个表存储巴士的信息，station_name, chukou和busName作为联合主键，分别代表这个站的名字，这个站的出口名称以及这个出口对应巴士的名字，其中station_name同时以外键形式存在指向station表。

**Table Name: out_info**

1. **Columns: ** id(pk), station_name(fk), outt, textt
2. **Description:** 这个表存储每个出口的信息，id是生成的从1开始的自增量作为主键，station_name作为外键指向station表；outt,textt是对out_info的额外描述。

**Table Name: card**

1. **Columns: ** code_id(pk), money, create_time
2. **Description:** 这个表存储每张卡的信息，code_id是表的主键，代表卡号；money代表卡的余额，create_time代表创建卡的时间。

**Table Name: passenger**

1. **Columns: ** id_number(pk), name, phone_number, gender, district
2. **Description:** 这个表存储乘客的信息，id_number是表的主键，代表乘车人的身份证号；无外键；剩余的列包括name等信息是对当前乘车人的描述。

**Table Name: passenger_ride**

1. **Columns: ** ride_id(pk), passenger_id(fk), start_staion(fk), end_station(fk), price, start_time, end_time
2. **Description:** 这个表存储所有以乘客身份证号记录的乘车情况，ride_id是自增的主键，仅代表条目；passenger_id作为外键指向passenger表，start_station和end_station也都是外键，均指向station表；其他列为其他描述。

**Table Name: card_ride**

1. **Columns: ** ride_id(pk), card_id(fk), start_staion(fk), end_station(fk), price, start_time, end_time
2. **Description:** 这个表存储所有以卡乘车号记录的乘车情况，ride_id是自增的主键，仅代表条目；card_id作为外键指向card表，start_station和end_station也都是外键，均指向station表；其他列为其他描述。

## 数据导入

### 导入数据之前

由于`.json`文件部分数据会导致导入数据产生问题，故在不改变数据本身真实性与准确性的基础上，我们对下列数据集进行了微调。

a. 删除重复

![image-20240422171831371](C:\Users\B_W_Y_Y\AppData\Roaming\Typora\typora-user-images\image-20240422171831371.png)

删除`stations.json`文件中重复"鹏兴实验学校"

b.名字微调

![image-20240427101542646](C:\Users\B_W_Y_Y\AppData\Roaming\Typora\typora-user-images\image-20240427101542646.png)

将`ride.json,stations.json,lines.json`中所有的`Dongjiang Column Memorial \nHall Station`替换为`Dongjiang Column Memorial Hall Station`

![image-20240427101651441](C:\Users\B_W_Y_Y\AppData\Roaming\Typora\typora-user-images\image-20240427101651441.png)

将`ride.json,stations.json,lines.json`中所有的`Huilongpu  station\n`替换为`Huilongpu station`

### 基本数据的导入

|   Script Name   | Auther |                         Description                          |
| :-------------: | :----: | :----------------------------------------------------------: |
|    cards.py     | 陈长信 |                将cards.json文件数据导入card表                |
| line_station.py | 陈长信 | 将lines.json文件中line_name和station_name的相关数据导入line_stations表 |
|    lines.py     | 陈长信 |            将lines.json文件中剩余数据导入lines表             |
|   station.py    | 陈长信 |      将stations.json文件部分与station直接相关的数据导入      |
|  passenger.py   | 陈长信 |           将passenger.json文件数据导入passenger表            |
|   bus_info.py   | 陈长信 | 将stations.json文件中关于busName,chukou等信息导入bus_info表  |
|   out_info.py   | 陈长信 | 将stations.json文件中每个station_name对应的outt,textt等出口信息导入out_info表 |
|     ride.py     | 陈长信 |    将ride.json文件数据导入passenger_ride和card_ride两个表    |

在进行了导入数据之前的修改之后，本部分主要通过Python对数据进行导入，主要使用`psycopg2`与`PostgreSQL`进行连接，然后利用`cursor`对数据进行逐行的插入，最后提交事务。另外，为了方便以及避免数据的重复，每次重新跑代码的时候会对原数据进行删除，下面以cards.py代码举例子说明。

````python
# 连接到 PostgreSQL 数据库
conn = psycopg2.connect(
    ....
)
cursor = conn.cursor()

# 这里在每次插入之前清空表中的数据，防止重复插入
cursor.execute("DELETE FROM card")
# 打开 JSON 文件并插入数据
with open('src/cards.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    # 插入数据
...(对code,money,create_time值进行更新)
        # 执行插入操作
        cursor.execute("INSERT INTO card (code_id, money, create_time) VALUES (%s, %s, %s )", (code, money, create_time))   
        
# 提交事务
conn.commit()
# 关闭连接
cursor.close()
conn.close()
````

这里采用一条一条的插入方式，效率较低，优化策略见后文（这里以`ride.json`文件的插入速度为样例进行了测试）。

![image-20240427205748990](C:\Users\B_W_Y_Y\AppData\Roaming\Typora\typora-user-images\image-20240427205748990.png)

### 数据准确性检查

本部分主要通过`SQL语句`对数据进行查询查找，具体实现见下列代码。

````sql
-- Q1
SELECT s.district,
       COUNT(*) AS station_count
FROM station s
GROUP BY s.district;-- 每个区域的站点数量
SELECT l.line_name,
       COUNT(ls.station_name) AS station_count
FROM lines l
         JOIN line_stations ls ON l.line_name = ls.line_name
GROUP BY l.line_name;-- 每条线路的站点数量
SELECT COUNT(*) AS total_station_count
FROM station;-- 总共的站点数量
-- Q2
SELECT COUNT(p.id_number) AS female_passenger_count
FROM passenger p
WHERE p.gender = '女';-- 女性乘客数量
SELECT COUNT(*) AS male_passenger_count
FROM passenger p
WHERE p.gender = '男';-- 男性乘客数量
-- Q3
SELECT CASE
           WHEN p.district LIKE '%Chinese Mainland%' THEN '中国大陆' WHEN p.district LIKE '%Chinese Hong Kong%' THEN '香港' WHEN p.district LIKE '%Chinese Macao%' THEN '澳门' WHEN p.district LIKE '%Chinese Taiwan%' THEN '台湾' ELSE '其他' END            AS region,
       COUNT(p.id_number) AS passenger_count
FROM passenger p
WHERE p.district LIKE '%Chinese Mainland%' OR p.district LIKE '%Chinese Hong Kong%' OR p.district LIKE '%Chinese Macao%' OR p.district LIKE '%Chinese Taiwan%'
GROUP BY region;-- 来自中国大陆、香港、澳门和台湾的乘客数量
-- Q4
SELECT DISTINCT a.busName, a.chukou AS exit, b.outt AS out_info_exit, b.textt AS landmark
FROM bus_info a
         JOIN out_info b ON a.chukou = b.outt AND a.station_name = b.station_name
WHERE a.station_name = 'Luohu';
-- Q5
SELECT pr.passenger_id, p.name AS passenger_name, pr.start_station, pr.end_station, pr.start_time, pr.end_time
FROM passenger_ride pr
         JOIN passenger p ON pr.passenger_id = p.id_number
WHERE pr.passenger_id = '230708194906183748';-- 特定乘客的旅程信息
-- Q6
SELECT cr.card_id, cr.start_station, cr.end_station, cr.start_time, cr.end_time
FROM card_ride cr
WHERE cr.card_id = '882132348';-- 特定旅行卡的乘车记录
-- Q7
SELECT s.station_name AS english_name, s.chinese_name AS chi_name, COUNT(e.outt)  AS exit_count, s.district, l.line_name
FROM station s
         JOIN line_stations ls ON s.station_name = ls.station_name
         JOIN lines l ON ls.line_name = l.line_name
         LEFT JOIN out_info e ON s.station_name = e.station_name -- 替换出口表为实际的表名
WHERE s.station_name = 'Luohu'
GROUP BY s.station_name, s.chinese_name, s.district, l.line_name;
-- Q8
SELECT l.line_name, l.start_time, l.end_time, l.first_opening, COUNT(DISTINCT ls.station_name) AS station_count, l.intro
FROM lines l
         JOIN line_stations ls ON l.line_name = ls.line_name
where l.line_name = '5号线'
GROUP BY l.line_name; -- -- 特定地铁线路的信息（假设 line_stations 表中的列名为 line_name）
````

### 优化与扩展

#### 使用MySQL数据库

在使用`PostgreSQL`数据库导入之后，我用相似的方法给`MySQL`数据库进行了导入。配置方法大体与前者相同，我配置了本地的`MySQL`环境，下载Server，进行了注册账户设置密码等操作，`user = root,Port = 3306`,并把DataGrip与`MySQL`连接，测试连接情况。

![image-20240427204315357](C:\Users\B_W_Y_Y\AppData\Roaming\Typora\typora-user-images\image-20240427204315357.png)

然后在创建的Project下`create schema project1`来创建Schema，`MySQL`的建表语句与`PostgreSQL`极其相似，这里略过描述，最后建好相似的表。然后在进行数据导入的时候，我也使用Python进行操作，利用`pymysql`与`MySQL`建立连接，然后同样利用cursor给`MySQL`的`Schema`中的表导入数据，具体的`.json`文件读取方式与`PostgreSQL`基本相似，故这里不过多赘述。同样的，我基于`ride.json`文件的导入速度进行测试，结果如下：

![image-20240427210128730](C:\Users\B_W_Y_Y\AppData\Roaming\Typora\typora-user-images\image-20240427210128730.png)

与给`PostgreSQL`相对比，速度相仿，`MySQL`略微慢一点。

#### 使用Java进行数据导入

上述均是使用Python进行数据导入，本板块旨在使用Java进行数据导入，为了与后续导入速度做铺垫，本部分利用`Batch`批量导入方式进行导入。

| Script Name | Auther |                    Description                     |
| :---------: | :----: | :------------------------------------------------: |
|  Main.java  | 赵欣瞳 | 将.json文件通过不同"try,catch"板块将数据导入数据库 |

代码使用了`JSONObject`和`JSONArray`来解析每个.json文件中的字符串，提取出需要插入到数据库的数据。

`try (Connection conn = DriverManager.getConnection(JDBC_URL, USER, PASSWORD))`执行数据库的连接并且在板块中执行数据导入操作。

其中使用了几个关键技术和优化方法来提高数据导入的效率和可靠性。代码在导入数据时采用了批量插入（Batch Insert）的优化方法，并使用PreparedStatement的方式执行插入操作。以下是对这段代码中使用的优化方法和导入数据方式的解释（同样使用`cards.json`的导入作为例子）

`List<Cards> cards = readJsonArray(Path.of(...),Card.class)`

**1.** **批处理（Batch Processing）的使用**

批量插入允许将多条SQL语句组合在一起，一次性发送给数据库执行，从而减少了与数据库的交互次数，提高了数据导入的效率。在这段代码中，`PreparedStatement`对象的`addBatch()`方法被用于将每次循环中的插入操作添加到批处理中，最后通过`executeBatch()`方法一次性执行所有批处理中的SQL语句。这种方式比单独执行每一条插入语句要快得多，特别是在处理大量数据时效果更为显著。这样做的好处是减少了与数据库的交互次数，提高了插入操作的性能。

**2. PreparedStatement的使用**

代码使用了`PreparedStatement`来执行SQL插入操作，而不是`Statement`。`PreparedStatement`是预编译的SQL语句，相比`Statement`，它更有优势的原因是由于SQL语句是预编译的，数据库可以缓存编译后的执行计划，从而减少了解析和优化SQL语句的开销。

```java
//.json文件读取
List<Cards> cards = readJsonArray(Path.of(...),Card.class);
importCardsToDatabase(cards);//这一段导入cards
private static void importCardsToDatabase(List<Cards> cards) {
    try (Connection conn = DriverManager.getConnection(JDBC_URL, USER, PASSWORD)) {
        conn.setAutoCommit(false); // 开启事务处理
        String insertSql = "INSERT INTO card (code_id, money, create_time) VALUES (?, ?, ?)";
        PreparedStatement pstmt = conn.prepareStatement(insertSql);
        for (Cards card : cards) {
            // 设置PreparedStatement的参数，根据Cards类的属性和数据库表的字段进行调整
            pstmt.setString(1, card.getCode());
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
```

利用上述的代码模式，同样我们对`ride.json`文件进行了写入速度测试，由于Java是分开读入的，所以这里对`passenger_ride`和`card_ride`分开进行了测试，最终得到以下结果

````javascript
data imported successfully
Import Time = 1377 ms
Loading Speed = 26504.7 records/s // card_ride
data imported successfully
Import Time = 2213 ms
Loading Speed = 28695.4 records/s // passenger_ride
Average Loading Speed = 27855.1 records/s
````

我们发现，相比较于逐条导入的Python方法，利用`Batch`批量导入的方法导入速度明显加快，对导入速度的优化分析见后续。

#### 导入方法优化（主要基于Python且只针对数据量较大的ride.json进行实验分析）

##### executemany()的使用

对读入的数据创建`passenger_data`和`card_data`两个list来存储有用信息，然后在所有数据填进list之后用`cursor.executemany()`批量进行插入操作。

````python
for...
	passenger_data.append((passenger_ride_id,user_id, start_station, end_station, price, start_time, end_time))
	card_data.append((card_ride_id,user_id, start_station, end_station, price, start_time, end_time))
# 批量插入数据
cursor.executemany("INSERT INTO passenger_ride (...) VALUES (...)", passenger_data)
cursor.executemany("INSERT INTO card_ride (...) VALUES (...)", card_data)
````

同样进行了测试，得到如下结果：

![image-20240428145210756](C:\Users\B_W_Y_Y\AppData\Roaming\Typora\typora-user-images\image-20240428145210756.png)

我们发现实际上只有小幅度的速度增长，并不符合预期。

##### Batch思路的运用以及与MySQL的比较

继续优化，使用`batch`优化，批量插入的大小设置为`batch_size = 10000`，相似的思路，在每次插入之后清空list，最后插入剩余的数据。

````python
for...
	if len(passenger_data_batch) >= batch_size:
		cursor.executemany()
		passenger_data_batch = [] ##清空list
	if len(card_data_batch) >= batch_size:
        cursor.executemany()
        card_data_batch = [] ##清空list
# 处理剩余数据
if passenger_data_batch:
    cursor.executemany()
if card_data_batch:
    cursor.executemany()
````

进行测试，速度依旧增长不大。

![image-20240428150047887](C:\Users\B_W_Y_Y\AppData\Roaming\Typora\typora-user-images\image-20240428150047887.png)

由于不符合预期，本来以为是代码本身出的问题，想到之前对`MySQL`已经完成了对数据的插入，决定对`MySQL`进行同样的测试。

首先是基本的`insert`，得到数据的确相仿。

![image-20240428151109012](C:\Users\B_W_Y_Y\AppData\Roaming\Typora\typora-user-images\image-20240428151109012.png)

接着遵循同样的优化策略，对使用`executemany`以及`Batch`的也分别进行了测试，仅是更改了数据库的连接信息，得到如下结果。

![image-20240428151400490](C:\Users\B_W_Y_Y\AppData\Roaming\Typora\typora-user-images\image-20240428151400490.png)

我们发现在对`MySQL`进行操作时候优化非常明显，为了更加直观见下图。

![image-20240428154016190](C:\Users\B_W_Y_Y\AppData\Roaming\Typora\typora-user-images\image-20240428154016190.png)

我们发现`MySQL`的优化效率惊人，提高了533%的速度。为什么会这样呢？我认为可能有以下两种原因：

a. **事务处理**：MySQL默认开启自动事务，也即每条SQL都会被当成一个事务，当插入非常多条数据时，每次都需要开启一次事务，事务的开销相比插入一条数据而言比例是非常高的，资源实际利用率是非常低的，而使用批量插入，只需开启一次事务，事务占用的开销比插入操作而言比例很小，资源实际利用率是很高的。

b. **内部优化**：MySQL 和 PostgreSQL 的数据库引擎可能在处理批量插入时采取了不同的内部优化策略，比如在处理插入操作时执行了更多的安全检查和约束验证，以确保数据的一致性和完整性。而MySQL 的存储引擎可能针对批量插入进行了更多的优化，以提高性能。

##### Copy_from方法

使用Copy_from方法相当于先把.json文件的数据读出到临时表中，最后使用Copy命令一次性进行读入，这样在处理大数据量的时候会有显著的优势。

代码大概思路是通过`pandas`提供的方法来读取、处理和写入数据文件，使用 `pandas` 将数据加载到 `DataFrame` 中，然后使用 `DataFrame` 的 `to_csv` 方法将数据保存到文件中。然后，你可以使用 `copy_from` 方法将文件中的数据加载到 PostgreSQL 数据库中的表中，以实现高效的数据加载操作。

````python
passenger_datas = pd.DataFrame(passenger_data)
card_datas = pd.DataFrame(card_data)

## 转换为流文件
f_passenger = StringIO()
f_card = StringIO()
## 写入.csv文件
passenger_datas.to_csv(f_passenger, sep='\t', index=False, header=False)
card_datas.to_csv(f_card, sep='\t', index=False, header=False)
## 指针移动到头部
f_passenger.seek(0)
f_card.seek(0)

## 使用copy_from写入数据库
cursor.copy_from(f_passenger, 'passenger_ride', columns=(...))
cursor.copy_from(f_card, 'card_ride', columns=(...))
````

进行测试结果如下

![image-20240428153745807](C:\Users\B_W_Y_Y\AppData\Roaming\Typora\typora-user-images\image-20240428153745807.png)

我们发现如我们所料，数据载入速度得到了显著提升，提升幅度达到了380%。那么为什么这个方法优化效果明显呢？我认为有以下原因：

1. **减少通信开销**：使用 `copy_from` 方法将数据直接加载到数据库中，可以减少数据库客户端和服务器之间的通信开销。在传统的逐条插入或使用 `executemany` 方法时，每条插入语句都需要与数据库进行一次通信，这会增加额外的网络延迟和开销。而 `copy_from` 方法在一次通信中就可以加载大量数据，从而减少了通信开销。
2. **减少约束检查**：当使用 `executemany` 方法插入大量数据时，数据库通常需要对每个插入操作进行索引和约束检查，而使用 `copy_from` 方法时，可以选择在加载数据之前禁用索引和约束检查，从而减少了这些额外的开销。

#### 数据集大小的扩展实验

我们针对ride.json文件进行拓展实验，通过Java对进行数据集的生成（数据均为随机捏造），仅作为导入速度的测试使用。

主要通过`generateRecord`进行数据的生成，使用了`BufferedWriter`来包装`FileWriter`，这有助于减少磁盘I/O操作，因为数据首先被写入缓冲区，然后一次性刷新到磁盘。为了避免并发写入时的数据冲突，并且在写入`BufferedWriter`时使用了`synchronized`块。具体代码请见`TravelRecordGenerator.java`。

````java
private static String generateRecord(int index, String[] stations, SimpleDateFormat sdf) {
	Random random = new Random(index); // Use the index as the seed for reproducibility (optional)
	return "{\"user\":\"" + random.nextLong() + "\"" + ",\"start_station\":\"" + getRandomStation(stations, random) + "\"" +  ",\"end_station\":\"" + getRandomStation(stations, random) + "\"" + ",\"price\":" + (random.nextInt(100) + 1) + ",\"start_time\":\"" + sdf.format(generateRandomDate(random)) + "\"" + ",\"end_time\":\"" + sdf.format(generateRandomDate(random)) + "\"}";
}
````

我们对数据集从`100000~1000000`进行了测试，得到了如下的导入时间结果。

````javascript
pass imported successfully.
程序运行时间(testcase = 100000): 2698 毫秒
程序运行时间(testcase = 200000): 5275 毫秒
程序运行时间(testcase = 300000): 7903 毫秒
程序运行时间(testcase = 400000): 10651 毫秒
程序运行时间(testcase = 900000): 23454 毫秒
程序运行时间(testcase = 900000): 25822 毫秒
程序运行时间(testcase = 1000000): 26575 毫秒
````

我们发现，导入数据时间与数据量总体大致成线性关系（由于篇幅有限这里略去图表呈现），另外，随着数据量增大，导入数据速度有所波动不过波动不大。

换算成导入速度（records/s），并做出图表，如下图所示。

![image-20240429131211292](C:\Users\B_W_Y_Y\AppData\Roaming\Typora\typora-user-images\image-20240429131211292.png)

我们发现，`Java`使用`Batch`的导入速度在不同数据集volumn的情况下速度相差不大，平均导入速度为`36141 records/s`

但是留意发现，通过我们生成的数据集导入速度却比导入项目原本的.json文件要快一些，我们认为可能的原因是：

在生成数据的时候，我们取消了Passenger_ride和passenger的外键约束，防止因为外键冲突无法导入数据，这样导入数据时不用检查外键约束，当然要更快，节省了很多开销，导入效率得到了提高。

#### 扩展部分总结

综上所述，我们通过Python,Java两种语言对数据进行了导入，还对不同数据库通过不同的导入方式进行了导入速度的测试分析，最后进行了对数据集的扩展为得到导入速度的普遍规律（单位records/s）

|       导入方法       | PostgreSQL | MySQL |
| :------------------: | :--------: | :---: |
|      普通insert      |    6675    | 6350  |
|     executemany      |    7120    | 38250 |
|        Batch         |    7300    | 42015 |
|      Copy_from       |   31775    |   /   |
|     Batch(Java)      |   27855    |   /   |
| Batch(Java,新数据库) |   36141    |   /   |

由于时间的限制，没有在Java中进行更多的基于不同方法不同数据库的测试，但是我相信更多的测试会带来更加有意思的数据，可以做出更多的分析。
