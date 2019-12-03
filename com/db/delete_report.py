#!/usr/bin/python3
# coding=gbk

import pymysql

# 打开数据库连接
from com.utils.UUIDUtil import UUIDUtil

db = pymysql.connect(host="192.168.6.14",port=3306, user="xiang", passwd="Jiugt@2019!@#", db="two_invoice_check",charset='utf8')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 查询语句


try:

         sql = "delete from t_scm_invoice_reports where inv_date = '2018-09-13'";
         cursor.execute(sql)


         sql = "delete from t_scm_invoice_reports_detail";
         cursor.execute(sql)
         db.commit()


except Exception as e:
    print(e)

# 关闭数据库连接
cursor.close()
db.close()