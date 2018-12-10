import requests
from bs4 import BeautifulSoup
from pymysql import MySQLError
from utiles import transfer_content


def insert_if_not_exist_theater(db, theater, city):
    schedule_id = query_theater_id(db, theater["name"], city["id"])
    if schedule_id == -1:
        insert_theater_record(db, theater, city)
        return query_theater_id(db, theater["name"], city["id"])
    else:
        return schedule_id


# 判断电影院记录是否存在，不存在则添加
def insert_theater_record(db, theater, city):
    print("START insert_theater_record: " + theater["name"] + " - " + city["name"])
    cursor = db.cursor()
    sql_insert_theater = "INSERT INTO theater(name, city_id, url) VALUES \
                    ('%s', '%d', '%s')" % (transfer_content(theater["name"]), city["id"], theater["url"])
    try:
        cursor.execute(sql_insert_theater)
        db.commit()
        print("insert success: " + theater["name"] + " - " + city["name"])
    except MySQLError as e:
        print("Caught a MySQLError Error while insert_theater_record: " + sql_insert_theater)
        print(e)
        # 如果发生错误则回滚
        db.rollback()


def query_theater_id(db, theater_name, city_id):
    print("START query_theater_id: " + theater_name + " - " + str(city_id))
    cursor = db.cursor()
    sql_select_theater_id = "SELECT id FROM theater WHERE name = '%s' AND city_id = '%s'" \
                                 % (transfer_content(theater_name), city_id)
    try:
        rowcount = cursor.execute(sql_select_theater_id)
        if rowcount > 0:
            return cursor.fetchone()[0]
        else:
            return -1
    except MySQLError as e:
        print("Caught a MySQLError Error while get_theater_id: " + sql_select_theater_id)


# theater
def query_all_theater_record(db):
    print("START query all theater records")
    theater_list = []
    cursor = db.cursor()
    sql_select_theater = "SELECT id, name, city_id, url FROM theater"
    try:
        cursor.execute(sql_select_theater)
        results = cursor.fetchall()
        for row in results:
            theater = {}
            theater['id'] = row[0]
            theater['name'] = row[1]
            theater['city_id'] = row[2]
            theater['url'] = row[3]

            theater_list.append(theater)
    except MySQLError as e:
        print("Error: query_all_theater_record : " + sql_select_theater)
        print(e)

    return theater_list


def query_theater_record_by_id(db, id):
    print("START query all theater records")
    theater_list = []
    cursor = db.cursor()
    sql_select_theater = "SELECT id, name, city_id, url FROM theater WHERE id >= %s " % (id)
    try:
        cursor.execute(sql_select_theater)
        results = cursor.fetchall()
        for row in results:
            theater = {}
            theater['id'] = row[0]
            theater['name'] = row[1]
            theater['city_id'] = row[2]
            theater['url'] = row[3]

            theater_list.append(theater)
    except MySQLError as e:
        print("Error: query_theater_record_by_id : " + sql_select_theater)
        print(e)

    return theater_list


def parse_theaters(name, city_url, start_url):
    # print(city_url)
    html = requests.get(city_url)
    soup = BeautifulSoup(html.content, "html.parser")

    theater_items = soup.find_all("div", class_="establishment")
    theater_list = []
    for theater_temp in theater_items:
        # print(i)
        theater = {}
        theater["name"] = theater_temp.find("a").text
        theater["url"] = start_url + theater_temp.find("a").get("href")
        # print(cinema)
        theater_list.append(theater)
    return theater_list
