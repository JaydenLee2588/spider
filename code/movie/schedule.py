import pymysql
import re
import requests
from bs4 import BeautifulSoup
from pymysql import ProgrammingError, MySQLError


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
