#!/usr/bin/python3
# coding=gbk

import pymysql

# �����ݿ�����
from com.utils.UUIDUtil import UUIDUtil

db = pymysql.connect(host="192.168.6.14",port=3306, user="xiang", passwd="nEw-TESt@&2#", db="two_invoice_check_dev",charset='utf8')

# ʹ��cursor()������ȡ�����α�
cursor = db.cursor()

# SQL ��ѯ���


try:
         code = "printStatus";
         desc = "��ӡ״̬";
         id = UUIDUtil.getUUID();
         sql = "INSERT into t_s_typegroup (id,TYPEGROUPCODE,TYPEGROUPNAME) values('"+id+"','"+code+"','"+desc+"');";
         cursor.execute(sql)


         dict = {'0':'δ��ӡ', '1':'�Ѵ�ӡ'}

         for key in dict.keys():
             kid = UUIDUtil.getUUID();
             sql = "INSERT into t_s_type (id,typecode,typename,typegroupid) values('"+kid+"','"+key+"','"+dict[key]+"','"+id+"')"
             cursor.execute(sql)
         db.commit()


except Exception as e:
    print(e)

# �ر����ݿ�����
db.close()