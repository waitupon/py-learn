#!/usr/bin/python3
# coding=gbk

import pymysql

# 打开数据库连接
db = pymysql.connect(host="39.96.86.145",port=3866, user="dev01", passwd="N23ni-#I1", db="token",charset='utf8')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 查询语句


try:

    for num in range(1000,20000):
         tax = "123" + str(num)
         sql = "INSERT INTO `token`.`tk_tax_user` (`taxno`) VALUES ('"+tax+"')";
         cursor.execute(sql)
         db.commit()


except:
    print("Error: unable to fetch data")

# 关闭数据库连接
db.close()