import pymysql.cursors

shop = 'Рога и копыта'
table = 'boarding_passes'


def get_connection():
    connection = pymysql.connect(host='***',
                                 user='***',
                                 password='***',
                                 db='arenda',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection
