import pymysql
import re
import requests
from bs4 import BeautifulSoup
from pymysql import ProgrammingError, MySQLError


# 判断电影记录是否存在，不存在则添加
def insert_cinema_record(db, cinema, city):
    # print("insert cinema recode")
    # print("---" + city["name"] + " --- " + city["url"])

    cursor = db.cursor()
    sql_select_city_id = "SELECT id FROM CITY WHERE name = '%s'" % (city["name"])
    try:
        # 获取city_id
        cursor.execute(sql_select_city_id)
        city_id = cursor.fetchone()[0]
        # print(city_id)

        sql_select_cinema = "SELECT * FROM cinema WHERE name = '%s' AND city_id= '%d'" % (cinema["name"], city_id)
        sql_insert_cinema = "INSERT INTO cinema(name, city_id, url) VALUES \
                ('%s', '%d', '%s')" % (cinema["name"], city_id, cinema["url"])

        # 判断是否存在cinema记录，不存在，则插入
        rowcount = cursor.execute(sql_select_cinema)
        if rowcount == 0:
            # 执行sql语句
            cursor.execute(sql_insert_cinema)
            # 提交到数据库执行
            db.commit()
            # print("insert success: " + cinema["name"])
        # else:
        #     print("exist:" + cinema["name"])
    except MySQLError as e:
        print("Caught a MySQLError Error: ")
        print(e)
        # 如果发生错误则回滚
        print("Insert cinema error: " + cinema["name"])

        db.rollback()


def parse_cinemas(name, city_url, start_url):
    # print(city_url)
    html = requests.get(city_url)
    soup = BeautifulSoup(html.content, "html.parser")

    cinema_items = soup.find_all("div", class_="establishment")
    cinema_list = []
    for i in cinema_items:
        # print(i)
        cinema = {}
        cinema["name"] = i.find("a").text
        cinema["url"] = start_url + i.find("a").get("href")
        # print(cinema)
        cinema_list.append(cinema)
    return cinema_list
