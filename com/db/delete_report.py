#!/usr/bin/python3
# coding=gbk

import pymysql

# �����ݿ�����
from com.utils.UUIDUtil import UUIDUtil

db = pymysql.connect(host="192.168.6.14",port=3306, user="xiang", passwd="Jiugt@2019!@#", db="two_invoice_check",charset='utf8')

# ʹ��cursor()������ȡ�����α�
cursor = db.cursor()

# SQL ��ѯ���


try:

         sql = "delete from t_scm_invoice_reports where inv_date = '2018-09-13'";
         cursor.execute(sql)


         sql = "delete from t_scm_invoice_reports_detail";
         cursor.execute(sql)
         db.commit()


except Exception as e:
    print(e)

# �ر����ݿ�����
cursor.close()
db.close()