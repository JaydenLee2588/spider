import requests
from bs4 import BeautifulSoup
from pymysql import MySQLError
from utiles import transfer_content


# 判断电影记录是否存在，不存在则添加
def insert_theater_hall_record(db, theater_hall_name, theater_id):
    cursor = db.cursor()

    sql_insert_theater_hall = "INSERT INTO theater_hall(hall_name, theater_id) VALUES \
                    ('%s', '%s')" % (transfer_content(theater_hall_name), theater_id)
    try:
        cursor.execute(sql_insert_theater_hall)
        db.commit()
        print("insert success: " + theater_hall_name)
    except MySQLError as e:
        print("Caught a MySQLError Error while insert_theater_hall_record: " + sql_insert_theater_hall)
        print(e)
        # 如果发生错误则回滚
        db.rollback()


#
def query_theater_hall_id(db, theater_hall_name):
    cursor = db.cursor()
    sql_select_theater_hall_id = "SELECT id FROM theater_hall WHERE hall_name = '%s'" \
                                 % (transfer_content(theater_hall_name))
    try:
        rowcount = cursor.execute(sql_select_theater_hall_id)
        if rowcount > 0:
            result = cursor.fetchone()
            hall_id = result[0]
        else:
            hall_id = -1
        return hall_id
    except MySQLError:
        print("Caught a MySQLError Error while query query_theater_hall_id: " + sql_select_theater_hall_id)


def insert_if_not_exist_theater_hall(db, theater_hall_name, theater_id):
    theater_hall_id = query_theater_hall_id(db, theater_hall_name)
    # print("==== theater_hall_id: " + str(theater_hall_id))
    if theater_hall_id == -1:
        insert_theater_hall_record(db, theater_hall_name, theater_id)
        return query_theater_hall_id(db, theater_hall_name)
    else:
        return theater_hall_id


# 获取cinema hall
def parse_theater_hall(theater_name, theater_url):
    print("get theater hall")
    html = requests.get(theater_url)
    soup = BeautifulSoup(html.content, "html.parser")

    theater_halls = []
    html_theater_halls = soup.find_all("li", class_="cinema")
    for html_hall in html_theater_halls:
        hall = {}
        # print("====\n" + html_hall.prettify())
        hall["theater_name"] = theater_name
        hall["name"] = html_hall.find("a", class_="link").get("alt")
        hall["url"] = html_hall.find("a", class_="link").get("href")
        theater_halls.append(hall)
    return theater_halls

