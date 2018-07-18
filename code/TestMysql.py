#!/usr/bin/python3

import pymysql

# 打开数据库连接
db = pymysql.connect(host="192.168.6.14",port=3306, user="xiang", passwd="nEw-TESt@&2#", db="two_invoice_check",charset='utf8')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 查询语句
sql = "SELECT * FROM t_scm_peers_goods"
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    for row in results:
        fname = row[0]
        lname = row[1]
        age = row[2]
        sex = row[3]
        income = row[4]
        print(row)
        # 打印结果
        # print("fname=%s,lname=%s,age=%d,sex=%s,income=%d"
        #       (fname, lname, age, sex, income))
except:
    print("Error: unable to fetch data")

# 关闭数据库连接
db.close()