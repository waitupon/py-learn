#!/usr/bin/python3
# coding=gbk

import pymysql

# 打开数据库连接
from com.utils.UUIDUtil import UUIDUtil

db = pymysql.connect(host="192.168.6.14",port=3306, user="xiang", passwd="Jiugt@2019!@#", db="two_invoice_check_dev",charset='utf8')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 查询语句


try:
         code = "specialInvRate";
         desc = "专票税率";
         id = UUIDUtil.getUUID();
         sql = "INSERT into t_s_typegroup (id,TYPEGROUPCODE,TYPEGROUPNAME) values('"+id+"','"+code+"','"+desc+"');";
         cursor.execute(sql)


         dict = {'17.00':'17.00', '13.00':'13.00','11.00':'11.00','6.00':'6.00','4.00':'4.00','3.00':'3.00'}

         for key in dict.keys():
             kid = UUIDUtil.getUUID();
             sql = "INSERT into t_s_type (id,typecode,typename,typegroupid) values('"+kid+"','"+key+"','"+dict[key]+"','"+id+"')"
             cursor.execute(sql)
         db.commit()


except Exception as e:
    print(e)

# 关闭数据库连接
cursor.close()
db.close()