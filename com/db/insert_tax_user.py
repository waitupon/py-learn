#!/usr/bin/python3
# coding=gbk

import pymysql

# �����ݿ�����
db = pymysql.connect(host="39.96.86.145",port=3866, user="dev01", passwd="N23ni-#I1", db="token",charset='utf8')

# ʹ��cursor()������ȡ�����α�
cursor = db.cursor()

# SQL ��ѯ���


try:

    for num in range(1000,20000):
         tax = "123" + str(num)
         sql = "INSERT INTO `token`.`tk_tax_user` (`taxno`) VALUES ('"+tax+"')";
         cursor.execute(sql)
         db.commit()


except:
    print("Error: unable to fetch data")

# �ر����ݿ�����
db.close()