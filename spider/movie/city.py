import requests
from bs4 import BeautifulSoup
from pymysql import MySQLError
from utiles import transfer_content


# 判断城市记录是否存在，不存在则添加
def insert_city_record(db, city):
    print("START insert city recode: " + city["name"])

    cursor = db.cursor()
    sql_select_city = "SELECT * FROM CITY WHERE name = '%s'" % (transfer_content(city["name"]))
    sql_insert_city = "INSERT INTO CITY(name, url) VALUES ('%s', '%s')" % (transfer_content(city["name"]), city["url"])
    try:
        rowcount = cursor.execute(sql_select_city)
        if rowcount == 0:
            # 执行sql语句
            cursor.execute(sql_insert_city)
            # 提交到数据库执行
            db.commit()
            print("insert success: " + city["name"])
        # else:
        #     print("exist:" + city["name"])
    except MySQLError as e:
        print("Caught a MySQLError Error while insert_city_record: " + sql_insert_city)
        print(e)
        # 如果发生错误则回滚
        db.rollback()


# 查询所有的city记录
def query_all_city_record(db):
    print("START query all city records")
    city_list = []
    cursor = db.cursor()
    sql_select_city = "SELECT id, name, url FROM CITY"
    try:
        cursor.execute(sql_select_city)
        results = cursor.fetchall()
        for row in results:
            city = {}
            city['id'] = row[0]
            city['name'] = row[1]
            city['url'] = row[2]

            city_list.append(city)
    except MySQLError as e:
        print("Error: query_all_city_record : " + sql_select_city)
        print(e)

    return city_list


def parse_cities(url):
    print("START pares cities : " + url)
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")

    city_items = soup.find("nav").find_all("li") #去掉前面几个链接
    city_list = []
    for i in city_items:
        if i.find("a").text == "Now Showing" or \
                i.find("a").text == "Upcoming Movies" or \
                i.find("a").text == "Trailers & Clips" or \
                i.find("a").text == "Near You" or \
                i.find("a").text == "Movies on TV":
            continue
        city = {}
        city["name"] = i.find("a").text
        city["url"] = i.find("a").get("href")
        city_list.append(city)

    return city_list
