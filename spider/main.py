import yaml
import pymysql

import city
import theater
import movie_detail
import schedule
import theater_hall

if __name__ == "__main__":
    f = open('config.yaml')
    config = yaml.load(f)

    db_info = config['mysql']
    db = pymysql.connect(db_info['ip'], db_info['user'], db_info['password'], db_info['database'])

    start_url = config['start_url']

    # 获取所有的city
    # city_list = city.parse_cities(start_url)
    # for city in city_list:
    #     print(city['name'])
    #     city.write_city_record_mysql(db, city)

    # 获取所有的theater
    # city_list = city.query_all_city_record(db)
    # for city_temp in city_list:
    #     print("=== city : " + city_temp['name'] + " ===")
    #     theater_list = theater.parse_theaters(db, city_temp['url'], start_url)
    #     for theater_temp in cinema_list:
    #         print("theater: " + theater_temp['name'] + " : " + theater_temp['url'])
    #         theater.insert_theater_record(db, theater_temp, city_temp)

    # 获取所有的theater hall

    # 获取movie detail
    # movie_detail_url = config["movie_detail_url"]
    # movie = movie_detail.parse_movie_detail(url)
    # movie_detail.insert_movie_detail_mysql(db, movie)

    # 获取schedule
    theater_name = config["theater_name"]
    theater_url = config["theater_url"]
    schedules = schedule.parse_schedule(theater_url)
    for schedule_temp in schedules:
        for movie_temp in schedule_temp["movies"]:
            print(schedule_temp["hall_name"] + " === " + movie_temp["name"] + " === " + schedule_temp["show_time"])
            schedule_temp["theater_id"] = theater.get_theater_id(db, theater_name, theater_url)
            schedule_temp["theater_hall_id"] = theater_hall.insert_if_not_exist_theater_hall(db, theater_name, theater_url)
            print("=====")
            schedule_temp["movie_id"] = movie_detail.insert_if_not_exist_movie(db, movie_temp["name"], movie_temp["detail_url"])
            schedule_temp["show_date"] = schedule_temp["show_time"][0, 9]
            schedule.insert_if_not_exist_schedule(db, schedule_temp)
