import psycopg2

host = 'rm-2zekfz97x1j87ora1.pg.rds.aliyuncs.com'
database = ''
user = ''
password = ''
port = 3433
conn = psycopg2.connect(host=host, port=port, user=user, password=password, database=database)
# connect()也可以使用一个大的字符串参数, 比如”host=localhost port=5432 user=postgres password=postgres dbname=test”
cursor = conn.cursor()
# 这里创建的是一个字典Cursor, 这样返回的数据, 都是字典的形式, 方便使用
sql = "DELETE FROM messagebox_message WHERE date_created  < '2019-07-01 00:00:00+08'"
cursor.execute(sql)
