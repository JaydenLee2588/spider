import pymysql
import re
import requests
from bs4 import BeautifulSoup
from pymysql import ProgrammingError, MySQLError


# 判断电影记录是否存在，不存在则添加
def write_movie_detail_mysql(db, movie):
    print("&&&&&")
    print("insert movie recode :" + movie.name)

    cursor = db.cursor()
    sql_select_movie_id = "SELECT id FROM movie WHERE name = '%s'" % (movie.name)
    try:
        sql_insert_movie = "INSERT INTO movie(name, mtrcbRating, genre, running_time) VALUES \
                    ('%s', '%s', '%s','%s')" % \
                    (movie.name, movie.mtrcbRating, movie.genre, movie.running_time)

        # 判断是否存在cinema记录，不存在，则插入
        rowcount = cursor.execute(sql_select_movie_id)
        if rowcount == 0:
            # 执行sql语句
            cursor.execute(sql_insert_movie)
            # 提交到数据库执行
            db.commit()
            print("insert success: " + movie.name)
        else:
            print("exist:" + movie.name)
    except MySQLError as e:
        print("Caught a MySQLError Error: ")
        print(e)
        # 如果发生错误则回滚
        print("Insert movie error: " + movie.name)

        db.rollback()


def exist_movie_detail(movie):
    cursor = db.cursor()
    sql_select_city = "SELECT * FROM movie WHERE name = '%s'" % (movie)
    try:
        rowcount = cursor.execute(sql_select_city)
        if rowcount == 0:
            # 执行sql语句
            return False
        else:
            return True
    except MySQLError:
        print("Caught a MySQLError Error while query exist_movie_detail: " + movie)


# 获取movie的detail
def get_movie_detail(url):
    print("get movie detail: " + url)

    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    movie = {}
    movie[""]
