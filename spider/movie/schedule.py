import requests
from bs4 import BeautifulSoup
from pymysql import MySQLError


def insert_if_not_exist_schedule(db, schedule):
    schedule_id = query_schedule_id(db, schedule)
    if schedule_id == -1:
        insert_schedule(db, schedule)
        return query_schedule_id(db, schedule)
    else:
        return schedule_id


def insert_schedule(db, schedule):
    cursor = db.cursor()
    sql_insert_schedule = "INSERT INTO movie_schedule(theater_id, theater_hall_id, movie_id, show_date, show_time)" \
                          " VALUES ('%s', '%s', '%s', '%s', '%s')" % \
                          (schedule["theater_id"], schedule["theater_hall_id"], schedule["movie_id"],
                           schedule["show_date"], schedule["show_time"])
    try:
        # 执行sql语句
        cursor.execute(sql_insert_schedule)
        # 提交到数据库执行
        db.commit()
        print("insert success: " + sql_insert_schedule)
    except MySQLError as e:
        print("Caught a MySQLError Error while Insert schedule error: " + sql_insert_schedule)
        print(e)
        # 如果发生错误则回滚
        db.rollback()


def query_schedule_id(db, schedule):
    cursor = db.cursor()
    sql_select_movie = "SELECT id FROM movie_schedule WHERE theater_id = '%s' " \
                       "AND theater_hall_id = '%s' " \
                       "AND movie_id = '%s' "\
                       "AND show_date = '%s' " \
                       "AND show_time = '%s' " % \
                       (schedule["theater_id"], schedule["theater_hall_id"], schedule["movie_id"],
                        schedule["show_date"], schedule["show_time"])
    try:
        rowcount = cursor.execute(sql_select_movie)
        if rowcount > 0:
            return cursor.fetchone()[0]
        else:
            return -1
    except MySQLError:
        print("Caught a MySQLError Error while query query_schedule_id: " + sql_select_movie)


# 获取movie的schedule
def parse_schedule(theater_url):
    print("START parse_schedule: " + theater_url)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
    html = requests.get(url=theater_url, headers=header)
    soup = BeautifulSoup(html.content, "html.parser")

    schedules = []

    html_theater_halls = soup.find_all("li", class_="cinema")
    for html_hall in html_theater_halls:
        schedule = {}

        # print(html_hall.prettify())
        schedule["hall_name"] = html_hall.find("a", class_="link")["alt"]
        schedule["hall_url"] = html_hall.find("a", class_="link")["href"]

        # html_movies
        movies = []
        for html_movie in html_hall.find_all("li"):
            movie = {}
            movie["detail_url"] = html_movie.select('a[itemprop=url]')[0].get("href")
            movie["name"] = html_movie.select('span[itemprop="name"]')[0].text
            # print(movie["name"] + " : " + movie["detail_url"])

            html_show_times = html_movie.find("div", class_="showtimes").find_all("meta")
            show_time = ""
            for html_show_time in html_show_times:
                show_time += html_show_time.get("content") + "; "
            schedule["show_time"] = show_time
            movies.append(movie)
        schedule["movies"] = movies

        schedules.append(schedule)
    return schedules
