import pymysql
import re
import requests
from bs4 import BeautifulSoup
from pymysql import ProgrammingError, MySQLError


# 判断电影院记录是否存在，不存在则添加
def insert_theater_record(db, theater, city):
    cursor = db.cursor()
    sql_select_city_id = "SELECT id FROM CITY WHERE name = '%s'" % (city["name"])
    try:
        # 获取city_id
        cursor.execute(sql_select_city_id)
        city_id = cursor.fetchone()[0]

        sql_select_theater = "SELECT * FROM theater WHERE name = '%s' AND city_id= '%d'" % (theater["name"], city_id)
        sql_insert_theater = "INSERT INTO theater(name, city_id, url) VALUES \
                ('%s', '%d', '%s')" % (theater["name"], city_id, theater["url"])

        # 判断是否存在cinema记录，不存在，则插入
        rowcount = cursor.execute(sql_select_theater)
        if rowcount == 0:
            # 执行sql语句
            cursor.execute(sql_insert_theater)
            # 提交到数据库执行
            db.commit()
            print("insert success: " + theater["name"])
        else:
            print("exist:" + theater["name"])
    except MySQLError as e:
        print("Caught a MySQLError Error: ")
        print(e)
        # 如果发生错误则回滚
        print("Insert cinema error: " + theater["name"])

        db.rollback()


def get_theater_id(db, theater_name, theater_url):
    print(theater_name + " : " + theater_url)
    cursor = db.cursor()
    sql_select_theater_hall_id = "SELECT id FROM theater WHERE name = '%s' AND url = '%s'" \
                                 % (theater_name, theater_url)
    try:
        # 获取theater_hall_id
        rowcount = cursor.execute(sql_select_theater_hall_id)

        if rowcount > 0:
            # 执行sql语句
            return cursor.fetchone()[0]
        else:
            return -1
    except MySQLError as e:
        print("Caught a MySQLError Error: ")
        print(e)


def parse_theaters(name, city_url, start_url):
    # print(city_url)
    html = requests.get(city_url)
    soup = BeautifulSoup(html.content, "html.parser")

    theater_items = soup.find_all("div", class_="establishment")
    theater_list = []
    for theater_temp in theater_items:
        # print(i)
        theater = {}
        theater["name"] = theater_temp.find("a").text
        theater["url"] = start_url + theater_temp.find("a").get("href")
        # print(cinema)
        theater_list.append(theater)
    return theater_list
