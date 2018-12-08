import requests
from bs4 import BeautifulSoup
from pymysql import MySQLError


# 判断电影记录是否存在，不存在则添加
def insert_movie_detail_mysql(db, movie):
    print("insert movie recode :" + movie["name"])

    cursor = db.cursor()
    sql_select_movie_id = "SELECT id FROM movie WHERE name = '%s'" % (movie["name"])
    try:
        sql_insert_movie = "INSERT INTO movie(name, year, mtrcb_rating, genre, duration, thumbnail_url, " \
                    "description, director, main_cast, writer, production_company) VALUES \
                    ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                    (movie["name"], movie["year"], movie["mtrcb_rating"], movie["genre"], movie["duration"],
                     movie["thumbnail_url"], movie["description"], movie["director"], movie["main_cast"],
                     movie["writer"], movie["production_company"])

        # 判断是否存在cinema记录，不存在，则插入
        rowcount = cursor.execute(sql_select_movie_id)
        if rowcount == 0:
            # 执行sql语句
            cursor.execute(sql_insert_movie)
            # 提交到数据库执行
            db.commit()
            print("insert success: " + movie["name"])
        else:
            print("exist:" + movie["name"])
    except MySQLError as e:
        print("Caught a MySQLError Error: ")
        print(e)
        # 如果发生错误则回滚
        print("Insert movie error: " + movie["name"])

        db.rollback()


def query_movie_id(db, movie_name, detail_url):
    cursor = db.cursor()
    sql_select_movie = "SELECT * FROM movie WHERE name = '%s' AND url = '%s'" % (movie_name, detail_url)
    try:
        rowcount = cursor.execute(sql_select_movie)
        if rowcount > 0:
            # 执行sql语句
            return cursor.fetchone()
        else:
            return -1
    except MySQLError:
        print("Caught a MySQLError Error while query query_movie_id: " + movie_name)


def insert_if_not_exist_movie(db, movie_name, movie_url):
    movie_id = query_movie_id(db, movie_name, movie_url)
    if movie_id == -1:
        movie = parse_movie_detail(movie_url)
        insert_movie_detail_mysql(movie)
        return query_movie_id(db, movie_name, movie_url)
    else:
        return movie_id


# 获取movie的detail
def parse_movie_detail(url):
    print("get movie detail: " + url)

    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    movie = {}
    detail_html = soup.find("div", id="container")
    # print(detail_html.prettify())
    movie["name"] = detail_html.find("h1").find("span", itemprop="name").text
    print("movie_name : " + movie["name"])
    movie["year"] = detail_html.find("h1").find("span", class_="year").text
    print("movie_year : " + movie["year"])
    movie["mtrcb_rating"] = detail_html.find("span", itemprop="contentRating").text
    print("movie_mtrcb_rating: " + movie["mtrcb_rating"])
    movie["genre"] = detail_html.find("span", itemprop="genre").text
    print("movie_genre: " + movie["genre"])
    movie["duration"] = detail_html.find("span", itemprop="duration").text
    print("movie_duration: " + movie["duration"])
    movie["thumbnail_url"] = detail_html.find("meta", itemprop="thumbnailUrl")["content"]
    print("movie_thumbnailUrl: " + movie["thumbnail_url"])
    movie["description"] = detail_html.find("div", itemprop="description").text
    print("movie_description: " + movie["description"])

    movie["main_cast"] = detail_html.find("dl", class_="moviedetail").dd.text
    print("movie_main_cast: " + movie["main_cast"])
    movie["director"] = detail_html.find("span", itemprop="director").text
    print("movie_director: " + movie["director"])
    movie["writer"] = detail_html.find("span", itemprop="author").text
    print("movie_writer: " + movie["writer"])
    movie["production_company"] = detail_html.find("span", itemprop="productionCompany").text
    print("movie_production_company: " + movie["production_company"])

    return movie
