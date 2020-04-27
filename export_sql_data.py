"""
根据sql 导出excel 数据
"""
import psycopg2
import xlsxwriter

from conf import db_conf

host = db_conf.host
user = db_conf.user
password = db_conf.password
database = db_conf.database
port = db_conf.port

filename = '项目成员.xlsx'
conn = psycopg2.connect(host=host, port=port, user=user, password=password, database=database)
# connect()也可以使用一个大的字符串参数, 比如”host=localhost port=5432 user=postgres password=postgres dbname=test”
cr = conn.cursor()
# 这里创建的是一个字典Cursor, 这样返回的数据, 都是字典的形式, 方便使用
sql = """
SELECT
    c.id 项目id,
    c.key 项目标识,
    c.remark 项目备注,
    cu.username 用户名,
    cu.first_name 用户姓名,
    cp.role 角色
FROM cmdb_projectmember cp
LEFT JOIN cmdb_project c ON cp.project_id = c.id
LEFT JOIN cmdb_user cu ON cp.user_id = cu.id
ORDER BY c.id
;
"""
cr.execute(sql)
data = cr.fetchall()
wbk = xlsxwriter.Workbook(filename=filename)
sheet = wbk.add_worksheet('sheet1')
row = 0
sheet.write_row(row, 0, [d.name for i, d in enumerate(cr.description)])
for d in data:
    row += 1
    sheet.write_row(row, 0, d)

wbk.close()
