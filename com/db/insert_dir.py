#!/usr/bin/python3
# coding=gbk

import pymysql

# 打开数据库连接
from com.utils.UUIDUtil import UUIDUtil

db = pymysql.connect(host="192.168.6.14",port=3306, user="xiang", passwd="nEw-TESt@&2#", db="two_invoice_check_dev",charset='utf8')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 查询语句


try:
         code = "printStatus";
         desc = "打印状态";
         id = UUIDUtil.getUUID();
         sql = "INSERT into t_s_typegroup (id,TYPEGROUPCODE,TYPEGROUPNAME) values('"+id+"','"+code+"','"+desc+"');";
         cursor.execute(sql)


         dict = {'0':'未打印', '1':'已打印'}

         for key in dict.keys():
             kid = UUIDUtil.getUUID();
             sql = "INSERT into t_s_type (id,typecode,typename,typegroupid) values('"+kid+"','"+key+"','"+dict[key]+"','"+id+"')"
             cursor.execute(sql)
         db.commit()


except Exception as e:
    print(e)

# 关闭数据库连接
db.close()