import requests
from bs4 import BeautifulSoup
from pymysql import MySQLError
from utiles import transfer_content


# 判断电影记录是否存在，不存在则添加
def insert_movie_detail(db, movie):
    print("start insert movie recode :" + movie["name"])

    sql_insert_movie = """INSERT INTO movie(name, year, mtrcb_rating, genre, duration, thumbnail_url, 
                        description, director, main_cast, writer, production_company) VALUES 
                        ('%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s')""" % \
                       (movie["name"], movie["year"],
                        movie["mtrcb_rating"], movie["genre"],
                        movie["duration"], movie["thumbnail_url"],
                        transfer_content(movie["description"]), movie["director"],
                        movie["main_cast"], movie["writer"],
                        movie["production_company"])
    cursor = db.cursor()
    try:
        # 执行sql语句
        cursor.execute(sql_insert_movie)
        # 提交到数据库执行
        db.commit()
        print("insert success: " + movie["name"])
    except MySQLError as e:
        print("Insert movie error: " + movie["name"])
        print("Insert movie script: " + sql_insert_movie)
        print(e)
        # 如果发生错误则回滚
        db.rollback()


def query_movie_id(db, movie_name):
    print("start query_movie_id: " + movie_name)
    cursor = db.cursor()
    sql_select_movie = "SELECT * FROM movie WHERE name = '%s' " % (movie_name)
    movie_id = -1
    try:
        rowcount = cursor.execute(sql_select_movie)
        if rowcount > 0:
            # 执行sql语句
            movie_id = cursor.fetchone()[0]

        print("finish query_movie_id: " + movie_name + ". movie_id is " + str(movie_id))
        return movie_id
    except MySQLError:
        print("Caught a MySQLError Error while query_movie_id: " + movie_name)


def insert_if_not_exist_movie(db, movie):
    print("enter insert_if_not_exist_movie : " + movie["name"])
    movie_id = query_movie_id(db, movie["name"])
    if movie_id == -1:
        insert_movie_detail(db, movie)
        return query_movie_id(db, movie["name"])
    else:
        return movie_id


# 获取movie的detail
def parse_movie_detail(url):
    print("start parse movie detail: " + url)

    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    movie = {}
    detail_html = soup.find("div", id="container")

    movie["name"] = detail_html.find("h1").find("span", itemprop="name").text
    try:
        movie["year"] = detail_html.find("h1").find("span", class_="year").text[1:5]
    except AttributeError:
        movie["year"] = "none"
    try:
        movie["mtrcb_rating"] = detail_html.find("span", itemprop="contentRating").text
    except AttributeError:
        movie["mtrcb_rating"] = "none"
    try:
        movie["genre"] = detail_html.find("span", itemprop="genre").text
    except AttributeError:
        movie["genre"] = "none"
    try:
        movie["duration"] = detail_html.find("span", itemprop="duration").text
    except AttributeError:
        movie["duration"] = "none"
    try:
        movie["thumbnail_url"] = detail_html.find("meta", itemprop="thumbnailUrl")["content"]
    except AttributeError:
        movie["thumbnail_url"] = "none"
    try:
        movie["description"] = detail_html.find("div", itemprop="description").text
    except AttributeError:
        movie["description"] = "none"
    try:
        movie["main_cast"] = detail_html.find("dl", class_="moviedetail").dd.text
    except AttributeError:
        movie["main_cast"] = "none"
    try:
        movie["director"] = detail_html.find("span", itemprop="director").text
    except AttributeError:
        movie["director"] = "none"
    try:
        movie["writer"] = detail_html.find("span", itemprop="author").text
    except AttributeError:
        movie["writer"] = "none"
    try:
        movie["production_company"] = detail_html.find("span", itemprop="productionCompany").text
    except AttributeError:
        movie["production_company"] = "none"

    print("movie_name: " + movie["name"] +
          "movie_year: " + movie["year"] +
          "movie_mtrcb_rating: " + movie["mtrcb_rating"] +
          "movie_genre: " + movie["genre"] +
          "movie_duration: " + movie["duration"] +
          "movie_thumbnailUrl: " + movie["thumbnail_url"] +
          "movie_description: " + movie["description"] +
          "movie_main_cast: " + movie["main_cast"] +
          "movie_director: " + movie["director"] +
          "movie_writer: " + movie["writer"] +
          "movie_production_company: " + movie["production_company"])

    return movie
