import pymysql
import re
import requests
from bs4 import BeautifulSoup
from pymysql import ProgrammingError, MySQLError


# 判断电影记录是否存在，不存在则添加
def write_cinema_hall_record_mysql(db, cinema_hall):
    cursor = db.cursor()
    sql_select_hall_id = "SELECT id FROM cinema_hall WHERE hall_name = '%s' and cinema_id = '%d'" % (cinema_hall["name"], cinema_hall["cinema_id"])
    try:
        sql_insert_cinema = "INSERT INTO cinema_hall(hall_name, cinema_id, url) VALUES \
                ('%s', '%d', '%s')" % (cinema_hall["name"], cinema_hall["cinema_id"], cinema_hall["url"])

        # 判断是否存在cinema_hall记录，不存在，则插入
        rowcount = cursor.execute(sql_select_hall_id)
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
        print("Insert cinema error: " + cinema_hall["name"])

        db.rollback()



def get_cinema_hall_id(hall_name, hall_url):
    cursor = db.cursor()
    sql_select_city = "SELECT id FROM ciname_hall WHERE hall_name = '%s' and url = '%s'" % (hall_name, hall_url)
    try:
        rowcount = cursor.execute(sql_select_city)
        if rowcount != 0:
            result = cursor.fetchone()
            hall_id = result[0]
            return hall_id
    except MySQLError:
        print("Caught a MySQLError Error while query exist_movie_detail: " + hall_name)


# 获取cinema hall
def get_cinema_hall(cinema_id, cinema_url):
    print("get cinema hall")
    html = requests.get(cinema_url)
    soup = BeautifulSoup(html.content, "html.parser")

    cinema_halls = []
    html_cinema_halls = soup.find_all("li", class_="cinema")
    for html_hall in html_cinema_halls:
        hall = {}
        # print("====\n" + html_hall.prettify())
        hall["cinema_id"] = cinema_id
        hall["name"] = html_hall.find("a", class_="link").get("alt")
        hall["url"] = html_hall.find("a", class_="link").get("href")
        cinema_halls.append(hall)
    return cinema_halls

