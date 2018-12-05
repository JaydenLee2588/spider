import pymysql
import re
import requests
from bs4 import BeautifulSoup
from pymysql import ProgrammingError, MySQLError

from movie import Movie


def get_cities(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")

    city_items = soup.find("nav").find_all("li") #去掉前面几个链接
    city_list = []
    for i in city_items:
        # print(i)
        if i.find("a").text == "Now Showing" or \
                i.find("a").text == "Upcoming Movies" or \
                i.find("a").text == "Trailers & Clips" or \
                i.find("a").text == "Near You" or \
                i.find("a").text == "Movies on TV":
            continue
        city = {}
        city["name"] = i.find("a").text
        city["url"] = i.find("a").get("href")
        # print(city)
        city_list.append(city)

    return city_list


def get_cinemas(name, url):
    print(url)
    html = requests.get(url)
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

# 逻辑要重新写，从movie的detail页面去获取movie的详细信息
def get_movies(url):
    # print(url)
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")

    schedule = soup.find("div", id="theatersArea")
    print(schedule)

    # for movies_content in soup.find_all(id="cinemas"):
        # print("===========\n" + movies_content.__str__())
        # print(type(movies_content))
        # print(movies_content.__sizeof__())

         # print("*** " + movies_content)
    # movie_items = soup.find_all("li", class_="cinema")
    # movie_list = []
    # for i in movie_items:
    #     # print(i)
    #     movie = Movie()
    #     movie.name = i.select('span[itemprop="name"]')[0].text
    #     movie.mtrcbRating = i.select('.mtrcbRating')[0].text
    #     movie.image = i.find("meta", itemprop="image", content=True)["content"]
    #     movie.genre = i.select('.genre')[0].text
    #     movie.running_time = i.select('.running_time')[0].text
    #
    #     for director in i.select('span[itemprop="director"]'):
    #         # print("---", director)
    #         movie.directors.append(director.text)
    #     print("movie : ", movie)
    #     movie_list.append(movie)
    #
    # return movie_list


# 获取movie的schedule
def get_schedule(cinema_url):
    print("get schedule")
    html = requests.get(cinema_url)
    soup = BeautifulSoup(html.content, "html.parser")

    schedule = []
    hall = []
    html_cinema_halls = soup.find_all("li", class_="cinema")
    for html_hall in html_cinema_halls:
        print(html_hall.prettify())
        hall["name"] = html_hall.find("a", class_="link").get("alt")
        hall["url"] = html_hall.find("a", class_="link").get("href")
        hall_id = get_cinema_hall_id(hall["name"], hall["url"])


        # html_movies
        movie_detail_url = html_hall.select('a[itemprop=url]')[1].get("href")
        movie_name = html_hall.select('span[itemprop="name"]')[0].text
        print(movie_name + " : " + movie_detail_url)
        if not exist_movie_detail(movie_name):
            movie = get_movie_detail(movie_detail_url)
            write_movie_detail_mysql(db, movie)
        html_show_times = html_hall.find("div", class_="showtimes").find_all("meta")
        for html_show_time in html_show_times:
            print(html_show_time)
            show_time = html_show_time.get("content")
            print("show_time : " + show_time)


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


# 获取movie的detail
def get_movie_detail(url):
    print("get movie detail: " + url)

    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    movie = {}
    movie[""]

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


# 判断城市记录是否存在，不存在则添加
def write_city_record_mysql(db, city):
    # print("insert city recode")
    # print("---" + city["name"] + " --- " + city["url"])

    cursor = db.cursor()
    sql_select_city = "SELECT * FROM CITY WHERE name = '%s'" % (city["name"])
    sql_insert_city = "INSERT INTO CITY(name, url) VALUES ('%s', '%s')" % (city["name"], city["url"])
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
        print("Caught a MySQLError Error: ")
        print(e)
        # 如果发生错误则回滚
        print("Insert city error: " + city["name"])

        db.rollback()


# 判断电影记录是否存在，不存在则添加
def write_cinema_record_mysql(db, cinema, city):
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


# 判断城市记录是否存在，不存在则添加
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

