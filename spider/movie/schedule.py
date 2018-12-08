import pymysql
import re
import requests
from bs4 import BeautifulSoup
from pymysql import ProgrammingError, MySQLError


def insert_if_not_exist_schedule(db, schedule):
    schedule_id = query_schedule_id(db, schedule)
    if schedule_id == -1:
        schedule = parse_schedule(schedule[""])
        insert_schedule(db, schedule)
        return query_schedule_id(db, schedule)
    else:
        return schedule_id


def insert_schedule(db, schedule):
    cursor = db.cursor()
    sql_insert_schedule = "INSERT INTO schedule(theater_id, theater_hall_id, movie_id, show_date, show_time)" \
                          " VALUES ('%s', '%s', '%s', '%s', '%s')" % \
                          (schedule["theater_id"], schedule["theater_hall_id"], schedule["movie_id"],
                           schedule["show_date"], schedule["show_time"])
    try:
        # 执行sql语句
        cursor.execute(sql_insert_schedule)
        # 提交到数据库执行
        db.commit()
        print("insert success: " + schedule["name"])
    except MySQLError as e:
        print("Caught a MySQLError Error: ")
        print(e)
        # 如果发生错误则回滚
        print("Insert city error: " + schedule["name"])

        db.rollback()


def query_schedule_id(db, schedule):
    cursor = db.cursor()
    sql_select_movie = "SELECT id FROM movie WHERE theater_id = '%s' " \
                       "AND theater_hall_id = '%s' " \
                       "AND movie_id = '%s' "\
                       "AND show_date = '%s'" \
                       "AND show_time = '%s'" % \
                       (schedule["theater_id"], schedule["theater_hall_id"], schedule["movie_id"],
                        schedule["show_date"], schedule["show_time"])
    try:
        rowcount = cursor.execute(sql_select_movie)
        if rowcount > 0:
            # 执行sql语句
            return cursor.fetchone()
        else:
            return -1
    except MySQLError:
        print("Caught a MySQLError Error while query query_movie_id: " + movie_name)


# 获取movie的schedule
def parse_schedule(theater_url):
    print("get schedule")
    html = requests.get(theater_url)
    soup = BeautifulSoup(html.content, "html.parser")

    schedules = []

    html_theater_halls = soup.find_all("li", class_="cinema")
    for html_hall in html_theater_halls:
        schedule = {}

        # print(html_hall.prettify())
        print(html_hall.find("a", class_="link")["alt"])
        schedule["hall_name"] = html_hall.find("a", class_="link")["alt"]
        schedule["hall_url"] = html_hall.find("a", class_="link")["href"]
        # hall_id = theater.get_theater_hall_id(hall_name, hall_url)

        # html_movies
        movies = []
        for html_movie in html_hall.find_all("li"):
            movie = {}
            movie["detail_url"] = html_movie.select('a[itemprop=url]')[1].get("href")
            movie["name"] = html_movie.select('span[itemprop="name"]')[0].text
            print(movie["name"] + " : " + movie["detail_url"])

            html_show_times = html_movie.find("div", class_="showtimes").find_all("meta")
            show_time = ""
            for html_show_time in html_show_times:
                # print(html_show_time)
                show_time += html_show_time.get("content") + "; "
                # print("show_time : " + show_time)
            schedule["show_time"] = show_time
            movies.append(movie)
        schedule["movies"] = movies

        schedules.append(schedule)
    return schedules
