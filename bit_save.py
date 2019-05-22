"""
存储文件
"""
import pymysql

# 连接数据库
db=pymysql.connect(host='localhost',
                   port=3306,
                   user='root',
                   password='123456',
                   database='stu',
                   charset='utf8')
# 获取游标
cur=db.cursor()

# 存储文件

# with open('hb.jpg','rb') as fd:
#     data=fd.read()
# try:
#     sql="insert into img values(1,'hb.jpg',%s)"
#     # print(sql,[data])
#     cur.execute(sql,[data])
#     db.commit()
#     # print(data)
# except Exception as e:
#     db.rollback()
#     print(e)

# 读取文件
sql="select*from img where filename='hb.jpg'"

cur.execute(sql)
img=cur.fetchone()
with open(img[1],'wb') as fd:
    fd.write(img[2])

cur.close()
db.close()
