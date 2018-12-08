import pymysql
import re
import requests
from bs4 import BeautifulSoup
from pymysql import ProgrammingError, MySQLError


# 判断电影记录是否存在，不存在则添加
def insert_theater_hall_record(db, theater_hall):
    cursor = db.cursor()
    sql_select_hall_id = "SELECT id FROM cinema_hall WHERE hall_name = '%s' and cinema_id = '%d'" % \
                         (theater_hall["name"], theater_hall["theater_id"])
    try:
        sql_insert_theater = "INSERT INTO cinema_hall(hall_name, cinema_id, url) VALUES \
                ('%s', '%d', '%s')" % (theater_hall["name"], theater_hall["theater_id"], theater_hall["url"])

        # 判断是否存在cinema_hall记录，不存在，则插入
        rowcount = cursor.execute(sql_select_hall_id)
        if rowcount == 0:
            # 执行sql语句
            cursor.execute(sql_insert_theater)
            # 提交到数据库执行
            db.commit()
            # print("insert success: " + theater["name"])
        # else:
        #     print("exist:" + theater["name"])
    except MySQLError as e:
        print("Caught a MySQLError Error: ")
        print(e)
        # 如果发生错误则回滚
        print("Insert cinema error: " + theater_hall["name"])

        db.rollback()


def query_theater_hall_id(db, theater_hall_name, theater_hall_url):
    cursor = db.cursor()
    sql_select_theater_hall_id = "SELECT id FROM theater_hall WHERE hall_name = '%s' and url = '%s'" % (theater_hall_name, theater_hall_url)
    try:
        rowcount = cursor.execute(sql_select_theater_hall_id)
        if rowcount > 0:
            hall_id = cursor.fetchone()
            # hall_id = result[0]
            return hall_id
    except MySQLError:
        print("Caught a MySQLError Error while query query_theater_hall_id: " + theater_hall_name)


def insert_if_not_exist_theater_hall(db, theater_name, theater_url):
    theater_hall_id = query_theater_hall_id(db, theater_name, theater_url)
    if theater_hall_id == -1:
        movie = parse_theater_hall(theater_url)
        insert_theater_hall_record(movie)
        return query_theater_hall_id(db, theater_name, theater_url)
    else:
        return theater_hall_id


# 获取cinema hall
def parse_theater_hall(theater_id, theater_url):
    print("get theater hall")
    html = requests.get(theater_url)
    soup = BeautifulSoup(html.content, "html.parser")

    theater_halls = []
    html_theater_halls = soup.find_all("li", class_="cinema")
    for html_hall in html_theater_halls:
        hall = {}
        # print("====\n" + html_hall.prettify())
        hall["theater_id"] = theater_id
        hall["name"] = html_hall.find("a", class_="link").get("alt")
        hall["url"] = html_hall.find("a", class_="link").get("href")
        theater_halls.append(hall)
    return theater_halls

