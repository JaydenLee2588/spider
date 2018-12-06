import yaml
import pymysql

import city
import cinema

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

    # 获取所有的cinema
    # city_list = city.query_all_city_record(db)
    # for city_temp in city_list:
    #     print("=== city : " + city_temp['name'] + " ===")
    #     cinema_list = cinema.parse_cinemas(db, city_temp['url'], start_url)
    #     for cinema_temp in cinema_list:
    #         print("cinema: " + cinema_temp['name'] + " : " + cinema_temp['url'])
    #         cinema.insert_cinema_record(db, cinema_temp, city_temp)
