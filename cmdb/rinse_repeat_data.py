"""
背景:资产信息中存在字段asset_id(实例id)重复的数据,直接删除时,由于级联关系存在,无法删除.故将asset_id根据重复次数依次添加后缀予以区分.
使用时需要修改主机地址等信息.
"""
import psycopg2

host = '127.0.0.1'
user = ''
password = ''
database = ''
port = 5432
conn = psycopg2.connect(host=host, port=port, user=user, password=password, database=database)
# connect()也可以使用一个大的字符串参数, 比如”host=localhost port=5432 user=postgres password=postgres dbname=test”
cursor = conn.cursor()
# 这里创建的是一个字典Cursor, 这样返回的数据, 都是字典的形式, 方便使用
sql = 'select id, asset_id FROM cmdb_asset WHERE id NOT IN (SELECT min(id) FROM cmdb_asset GROUP BY asset_id)'
cursor.execute(sql)
assets = cursor.fetchall()
repeat_data = {}
for asset in assets:
    if asset[1] in repeat_data.keys():
        repeat_data[asset[1]] += 1
        value = '%s_repeat_%s' % (asset[1], str(repeat_data[asset[1]]))
        update_sql = "update cmdb_asset set asset_id = '%s' WHERE id = %s" % (value,  asset[0])
        print(asset[0], asset[1], value)
        cursor.execute(update_sql)
    else:
        repeat_data[asset[1]] = 2
        value = '%s_repeat_%s' % (asset[1], 2)
        update_sql = "update cmdb_asset set asset_id = '%s' WHERE id = %s" % (value, asset[0])
        print(asset[0], asset[1], value)
        cursor.execute(update_sql)
conn.commit()
print(repeat_data)


