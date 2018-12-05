import yaml

import pymysql


if __name__ == "__main__":
    f = open('config.yaml')
    config = yaml.load(f)

    db_info = config['mysql']
    db = pymysql.connect(db_info['ip'], db_info['user'], db_info['password'], db_info['database'])
