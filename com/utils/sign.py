#!/usr/bin/env Python
# coding=utf-8

import hashlib
import hmac

import datetime
import requests
from flask import Flask, request, render_template
import json
import uuid
#import cx_Oracle
import pymysql

app = Flask(__name__)

@app.route('/myip')
def myip():
    ip = request.remote_addr
    return ip

@app.route('/sign')
def sign():
    accessKeyID = request.args.get("AccessKeyID")
    signatureNonce = request.args.get("SignatureNonce")
    timeStamp = request.args.get("TimeStamp")
    version = request.args.get("Version")
    key = request.args.get("key").strip()
    if accessKeyID is None or signatureNonce is None or version is None or key is None:
        return "param is illegal!"
    if timeStamp is None:
        data = "AccessKeyID=" + accessKeyID.strip() + "&SignatureNonce=" + signatureNonce.strip() + "&Version=" + version.strip()
    else:
        data = "AccessKeyID=" + accessKeyID.strip() + "&SignatureNonce=" + signatureNonce.strip() + "&TimeStamp=" + timeStamp.strip() + "&Version=" + version.strip()
    # sh_cmd = "java -jar /Users/tangyangyang/PycharmProjects/sign/signature.jar " + data + " " + key
    # p1 = subprocess.getoutput(sh_cmd)
    # arrp = p1.split(",")
    a = hmac.new(key.encode('utf-8'), data.encode('utf-8'), hashlib.sha1)
    m1 = hashlib.md5()
    m1.update(a.digest())
    sig = m1.hexdigest()
    print(data)
    print(sig)

    td = {'key': key, 'sign': sig}
    print(td)
    return json.dumps(td)


@app.route('/time')
def nowTime():
    nowTime = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    accessKeyID = request.args.get("AccessKeyID")
    key = request.args.get("key")
    if accessKeyID is None or key is None:
        return "param is illegal!"
    signatureNonce = str(uuid.uuid1()).replace("-", "")
    data = "AccessKeyID=" + accessKeyID.strip() + "&SignatureNonce=" + signatureNonce.strip() + "&Version=1.0"
    a = hmac.new(key.encode('utf-8'), data.encode('utf-8'), hashlib.sha1)
    m1 = hashlib.md5()
    m1.update(a.digest())
    sig = m1.hexdigest()
    sn = str(uuid.uuid1()).replace("-", "")
    try:
        url = "http://192.168.6.52/jxindependent/api/getTime?AccessKeyID=" + accessKeyID + "&SignatureNonce=" + signatureNonce + "&Version=1.0&Signature=" + sig
        reqjson = json.loads(requests.get(url).text)
        if "20" in reqjson:
            time = reqjson["model"]["SystemTime"]
        else:
            time = nowTime
        nt = {'tm': time, 'sn': sn}
        return json.dumps(nt)
    except:
        nt = {'tm': "52 server error!"}
        return json.dumps(nt)


@app.route('/sn')
def sn():
    sn = uuid.uuid1()
    uid = {'sn': str(sn).replace("-", "")}
    return json.dumps(uid)


@app.route('/delaccount')
def delaccount():
    invkind = request.args.get("invkind")
    invnum = request.args.get("invnum")
    accno = request.args.get("accno")
    db = request.args.get("db")
    if invkind is None or invnum is None or accno is None:
        return "param is illegal! invkind,invnum,accno,db"
    invkind = invkind.strip()
    invnum = invnum.strip()
    accno = accno.strip()

    def select_by_inv_num(cur, invkind, invnum):
        select_query = "select 1 from t_scm_vat_main_extend where inv_kind='" + invkind.strip() + "' and inv_num ='" + invnum + "' and ACCOUNTTING_NO='" + accno + "'"
        # select_query = "select 1"
        rl_sql = select_query
        print(rl_sql)
        cur.execute(rl_sql)
        is_exists_num = cur.fetchone()
        if is_exists_num is not None:
            return is_exists_num[0]
        else:
            return None

    def del_by_accno(cur, invkind, invnum, accno):
        del_query = "delete from t_scm_vat_main_extend where inv_kind='" + invkind + "' and inv_num ='" + invnum + "' and ACCOUNTTING_NO='" + accno + "'"
        rl_sql = del_query
        print(rl_sql)
        cur.execute(rl_sql)
    if db == "52":
        conn = pymysql.connect(host='192.168.6.62', user='root', passwd='baijia*58', db='jxstanded', port=3306,
                           charset='utf8')
    elif db == "223":
        pass
        #conn = cx_Oracle.connect('jxstanded/jxstanded@192.168.0.245:1521/csdb')  # 1个参数
    else:
        return "db error,must be [52 | 223]"

    cur = conn.cursor()

    result_of_select_num = select_by_inv_num(cur, invkind, invnum)
    if result_of_select_num is None:
        pass
    else:
        del_by_accno(cur, invkind, invnum, accno)
    cur.close()
    conn.commit()
    conn.close()
    return "init OK"


@app.route('/initmysql')
def initmysql():
    # taxno is 91110108339805094M
    invkind = request.args.get("invkind")
    invnum = request.args.get("invnum")
    invtype = request.args.get("invtype")
    taxno = request.args.get("taxno")
    if invkind is None or invnum is None or invtype is None or taxno is None:
        return "param is illegal!invkind,invnum,invtype,taxno"
    invkind = invkind.strip()
    invnum = invnum.strip()
    invtype = invtype.strip()
    taxno = taxno.strip()

    def select_by_inv_num(cur, invkind, invnum):
        select_query = "select 1 from t_scm_vat_main where inv_kind='" + invkind + "' and inv_num ='" + invnum + "'"
        # select_query = "select 1"
        rl_sql = select_query
        print(rl_sql)
        cur.execute(rl_sql)
        is_exists_num = cur.fetchone()
        if is_exists_num is not None:
            return is_exists_num[0]
        else:
            return None

    def update_inv(cur, taxno, invkind, invnum, invtype):
        update_query = "update T_SCM_VAT_MAIN t set t.BUYER_TAXNO='" + taxno + "',t.inv_type='" + invtype + "',t.INV_CONFIRM_STATUS=0,t.INV_DEDU_RESULT=0,t.PRE_DEDUCT_FLAG=0,t.TOLLSIGN='06'  where t.inv_kind='" + invkind + "' and t.inv_num='" + invnum + "'"
        rl_sql = update_query
        print(rl_sql)
        cur.execute(rl_sql)

    def insert_inv(cur, taxno, invkind, invnum, invtype):
        insert_query = "INSERT INTO t_scm_vat_main (BUYER_TAXNO, INV_KIND, INV_NUM, SELLER_TAXNO, INV_DATE, INV_COST, INV_VAT, INV_SUM, INV_RATE, INV_PWD, INV_DEDU_RESULT, INV_TYPE, INV_FROM, INV_STATUS, SCAN_MATCH, MATCH_STATUS, INV_TAX_SIGN, INV_COMMENT, INV_ERR_INFO, INV_DEDU_DATE, INV_CONFIRM_DATE, INV_CONFIRM_USER, INV_SEND_TIME, INV_RECE_TIME, SCAN_DATE, SCAN_USER, SCAN_NO, INV_INPUT_USER, INV_INPUT_TIME, INV_DRAW_TIME, INV_SCAN_TIME, BUYER_NAME, BUYER_ADDR_TEL, BUYER_BANK, SELLER_NAME, SELLER_ADDR_TEL, SELLER_BANK, MATCH_NO, MATCH_DATE, MATCH_USER, MATCH_ERR_INFO, SELLER_ID, PO_IDS, PO_TYPE, INV_TAXNO, SCAN_BATCH, CHGRES_USER, CHGRES_TIME, ERR_UPDATE_TIME, IS_TRANS, MATCH_COST, MATCH_VAT, FULL_CODE, FLOW_STATUS, CREATE_DATE, CREATE_BY, UPDATE_DATE, UPDATE_BY, INCOME_MONTH, RECORD_MONTH, INV_CONFIRM_STATUS, IMG_PATH, IMG_TIME, IS_COLLECT_ALL, COLLECT_TIME, IS_SCANNER, DEDU_INFO, UPDATE_DEDU_INFO_DATE, RECEV_FLAG, SCAN_UPDATE_DATE, SYS_COMPANY_CODE, SYNC_TASKNO, SYNC_SEND_STATUS, SIGN_TASKNO, SIGN_SEND_STATUS, DEDU_TASKNO, DEDU_SEND_STATUS, DEDU_APPLY_TASKNO, SYS_ORG_CODE, CHECK_TIME, RECEV_WAY, IS_TAXNO_FILL, APPLY_CONFIRM_TASKNO, CHECK_CODE, MACHINE_CODE, RECEIVING_CLERK, TOTAL_AMOUNT_CN, FULL_BUYER_TAXNO, PRE_DEDUCT_FLAG, TOLLSIGN, ZEROTAXRATESIGN, CHECK_ERR_CODE, IS_SAME_TAXINFO, ACCOUNT_TIME, VOUCHER_NUM, CERTIFICATION_WAY, CERTIFICATION_TYPE, IS_AGENCY_REBATE) " \
                       "VALUES(' " + taxno + "','" + invkind + "','" + invnum + "','91310114666025597Y','2017-09-21 16:00:00','7921.37','1346.63','9268.00',NULL,NULL,'0','" + invtype + "','4','0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'123',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,'0',NULL,NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL,'testet',NULL,'0',NULL,NULL,NULL,NULL,NULL,'testet',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'06',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);"
        rl_sql = insert_query
        print(rl_sql)
        cur.execute(rl_sql)

    conn = pymysql.connect(host='192.168.6.62', user='root', passwd='baijia*58', db='jxstanded', port=3306, charset='utf8')
    cur = conn.cursor()

    result_of_select_num = select_by_inv_num(cur, invkind, invnum)
    if result_of_select_num is None:
        insert_inv(cur, taxno, invkind, invnum, invtype)
    else:
        update_inv(cur, taxno, invkind, invnum, invtype)
    cur.close()
    conn.commit()
    conn.close()
    return "init OK"


@app.route('/initdedusql')
def inidedusql():
    invkind = request.args.get("invkind")
    invnum = request.args.get("invnum")
    invtype = request.args.get("invtype")
    db = request.args.get("db")
    taxno = request.args.get("taxno")

    if invkind is None or invnum is None or invtype is None or db is None:
        return "param is illegal!invkind,invnum,invtype,db,taxno"
    invkind = invkind.strip()
    invnum = invnum.strip()
    invtype = invtype.strip()
    db = db.strip()

    if invtype == "01":
        invid = "999999"
    elif invtype == "04":
        invid = "999998"
    elif invtype == "14":
        invid = "999997"
    else:
        return "inv type error!"

    # def del_inv_bynum(invkind, invnum):
    #     del_query = "delete from T_SCM_VAT_MAIN t WHERE t.inv_kind=" + invkind + " and inv_num=" + invnum
    #     print("del_inv_bynum")
    #     print(del_query)
    #     cursor.execute(del_query)
    #     conn.commit()

    def del_inv_id(invid):
        del_query = "delete from T_SCM_VAT_MAIN t WHERE id = " + invid
        print("del_inv_id")
        print(del_query)
        cursor.execute(del_query)
        conn.commit()

    def select_inv_bynum(invkind, invnum):
        select_query = "select 1 from T_SCM_VAT_MAIN t  where t.INV_KIND=" + invkind + " and t.inv_num = " + invnum
        print("select_inv_bynum:")
        print(select_query)
        cursor.execute(select_query)
        reslut_query_num = cursor.fetchone()
        return reslut_query_num

    def select_inv_byid(invid):
        select_query = "select 1 from T_SCM_VAT_MAIN t  where 1=1 and t.id=" + invid
        print("select_inv_byid:")
        print(select_query)
        cursor.execute(select_query)
        reslut_query_id = cursor.fetchone()
        return reslut_query_id

    def update_inv_num(invtype, invkind, invnum):
        print("inv num exists")
        update_query_num = "update T_SCM_VAT_MAIN t set t.BUYER_TAXNO='" + taxno + "',t.inv_type='" + invtype + "',t.INV_CONFIRM_STATUS=0,t.INV_DEDU_RESULT=0,t.PRE_DEDUCT_FLAG=0  where t.inv_kind=" + invkind + " and t.inv_num=" + invnum
        print("update_inv_num:")
        print(update_query_num)
        cursor.execute(update_query_num)
        conn.commit()

    def update_inv_id(invid, invtype, invkind, invnum):
        print("inv id exists")
        update_query_id = "update T_SCM_VAT_MAIN t set t.BUYER_TAXNO='" + taxno + "',t.inv_type='" + invtype + "',t.INV_CONFIRM_STATUS=0,t.INV_DEDU_RESULT=0,t.PRE_DEDUCT_FLAG=0,t.inv_kind='" + invkind + "',t.inv_num='" + invnum + "'  where t.id=" + invid
        print("update_inv_id:")
        print(update_query_id)
        cursor.execute(update_query_id)
        conn.commit()

    def insert_inv(invid, invtype, invkind, invnum):
        insert_query = "INSERT INTO T_SCM_VAT_MAIN (\"ID\", \"BUYER_TAXNO\", \"INV_KIND\", \"INV_NUM\", \"SELLER_TAXNO\", \"INV_DATE\", \"INV_COST\", \"INV_VAT\", \"INV_SUM\", \"INV_RATE\", \"INV_PWD\", \"INV_DEDU_RESULT\", \"INV_TYPE\", \"INV_FROM\", \"INV_STATUS\", \"SCAN_MATCH\", \"MATCH_STATUS\", \"INV_TAX_SIGN\", \"INV_COMMENT\", \"INV_ERR_INFO\", \"INV_DEDU_DATE\", \"INV_CONFIRM_DATE\", \"INV_CONFIRM_USER\", \"INV_SEND_TIME\", \"INV_RECE_TIME\", \"SCAN_DATE\", \"SCAN_USER\", \"SCAN_NO\", \"INV_INPUT_USER\", \"INV_INPUT_TIME\", \"INV_DRAW_TIME\", \"INV_SCAN_TIME\", \"BUYER_NAME\", \"BUYER_ADDR_TEL\", \"BUYER_BANK\", \"SELLER_NAME\", \"SELLER_ADDR_TEL\", \"SELLER_BANK\", \"MATCH_NO\", \"MATCH_DATE\", \"MATCH_USER\", \"MATCH_ERR_INFO\", \"SELLER_ID\", \"PO_IDS\", \"PO_TYPE\", \"INV_TAXNO\", \"SCAN_BATCH\", \"CHGRES_USER\", \"CHGRES_TIME\", \"ERR_UPDATE_TIME\", \"IS_TRANS\", \"MATCH_COST\", \"MATCH_VAT\", \"FULL_CODE\", \"FLOW_STATUS\", \"CREATE_DATE\", \"CREATE_BY\", \"UPDATE_DATE\", \"UPDATE_BY\", \"INCOME_MONTH\", \"RECORD_MONTH\", \"INV_CONFIRM_STATUS\", \"IMG_PATH\", \"IMG_TIME\", \"IS_COLLECT_ALL\", \"COLLECT_TIME\", \"IS_SCANNER\", \"DEDU_INFO\", \"UPDATE_DEDU_INFO_DATE\", \"RECEV_FLAG\", \"SCAN_UPDATE_DATE\", \"SYS_COMPANY_CODE\", \"SYNC_TASKNO\", \"SYNC_SEND_STATUS\", \"SIGN_TASKNO\", \"SIGN_SEND_STATUS\", \"DEDU_TASKNO\", \"DEDU_SEND_STATUS\", \"DEDU_APPLY_TASKNO\", \"SYS_ORG_CODE\", \"CHECK_TIME\", \"RECEV_WAY\", \"IS_TAXNO_FILL\", \"APPLY_CONFIRM_TASKNO\", \"CHECK_CODE\", \"MACHINE_CODE\", \"RECEIVING_CLERK\", \"TOTAL_AMOUNT_CN\", \"FULL_BUYER_TAXNO\", \"PRE_DEDUCT_FLAG\", \"TOLLSIGN\", \"ZEROTAXRATESIGN\", \"CHECK_ERR_CODE\", \"IS_SAME_TAXINFO\") VALUES ('" + invid + "', '10000001', '" + invkind + "', '" + invnum + "', '" + taxno + "', TO_DATE('2018-03-28 00:00:00', 'SYYYY-MM-DD HH24:MI:SS'), '36792.45', '370.51', '2550', NULL, NULL, '0', '" + invtype + "', '4', '2', NULL, NULL, NULL, NULL, NULL, NULL, TO_DATE('2018-03-29 17:55:04', 'SYYYY-MM-DD HH24:MI:SS'), 'dedu_interface', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '1','1','1', '1111111111111111111111111111111111', '11111111111111111111111111111 021-62290630', '11111111111111111111111111111111111111111bank', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, TO_DATE('2018-01-18 13:10:01', 'SYYYY-MM-DD HH24:MI:SS'), NULL, NULL, NULL, NULL, NULL, TO_DATE('2018-01-18 13:10:01', 'SYYYY-MM-DD HH24:MI:SS'), NULL, TO_DATE('2018-01-26 19:12:03', 'SYYYY-MM-DD HH24:MI:SS'), 'systemauto', '201803', NULL, '2', NULL, NULL, '1', NULL, NULL, NULL, NULL, NULL, NULL, '999999999', '51-20180330102154', '0', NULL, NULL, NULL, NULL, '98-20180329175500', '140845', TO_DATE('2018-01-26 19:12:03', 'SYYYY-MM-DD HH24:MI:SS'), NULL, NULL, NULL, '61735318311330084015', '661404205001', NULL, '1111111111111111', NULL, '0', NULL, NULL, NULL, NULL)"
        print("insert_inv:")
        print(insert_query)
        cursor.execute(insert_query)
        conn.commit()

    if db == "223":
        pass
        #conn = cx_Oracle.connect('jxstanded/jxstanded@192.168.0.245:1521/csdb')  # 1个参数
    elif db == "16":
        pass
        #conn = cx_Oracle.connect('bxjx/bxjx@192.168.7.170:1521/orcl')  # 1个参数
    else:
        return "db error"

    cursor = conn.cursor()

    result_of_select_num = select_inv_bynum(invkind, invnum)
    if result_of_select_num is None:
        result_of_select_id = select_inv_byid(invid)
        if result_of_select_id is None:
            insert_inv(invid, invtype, invkind, invnum)
        else:
            update_inv_id(invid, invtype, invkind, invnum)
    else:
        update_inv_num(invtype, invkind, invnum)

    cursor.close()
    conn.close()
    return "init OK"


@app.route('/setonestep')
def setonestep():
    tenant = request.args.get("tenant")
    flag = request.args.get("flag")
    db = request.args.get("db")

    if tenant is None or flag is None or db is None:
        return "param is illegal!tenant,flag,db"
        tenant = tenant.strip()
    flag = flag.strip()
    db = db.strip()

    def select_on_step(tenant):
        select_query = "select value from t_scm_config t where tenantid='" + tenant + "' and t.code='one_step_certify'"
        cursor.execute(select_query)
        reslut_query_step = cursor.fetchone()
        return reslut_query_step

    def insert_one_step(tenant, flag):
        cursor.execute("select max(id) from t_scm_config")
        reslut_query_getid = cursor.fetchone()
        if reslut_query_getid is None:
            stepid = "1"
        else:
            stepid = reslut_query_getid[0] + 1

        if flag == "1":
            insert_one_step = "insert into t_scm_config (ID, CODE, VALUE, USERID, TENANTID) values (" + stepid + ", 'one_step_certify', '1', null, '999999999')"
        else:
            insert_one_step = "insert into t_scm_config (ID, CODE, VALUE, USERID, TENANTID) values (" + stepid + ", 'one_step_certify', '0', null, '999999999')"
        cursor.execute(insert_one_step)
        conn.commit()

    def update_one_step(tenant, flag):
        if flag == "1":
            update_sql_step = "update t_scm_config set value = '1' where tenantid = '" + tenant + "' and code = 'one_step_certify'"
        else:
            update_sql_step = "update t_scm_config set value = '0' where tenantid = '" + tenant + "' and code = 'one_step_certify'"
        cursor.execute(update_sql_step)
        conn.commit()

    if db == "223":
        pass
        #conn = cx_Oracle.connect('jxstanded/jxstanded@192.168.0.245:1521/csdb')  # 1个参数
    elif db == "16":
        pass
        #conn = cx_Oracle.connect('bxjx/bxjx@192.168.7.170:1521/orcl')  # 1个参数
    elif db == "52":
        conn = pymysql.connect(host='192.168.6.62', user='root', passwd='baijia*58', db='jxstanded', port=3306, charset='utf8')
        cur = conn.cursor()
        cur.execute("select 1 from t_scm_config t where tenantid = '" + tenant + "' and code = 'one_step_certify'")
        if cur.fetchone() is None:
            if flag == "1":
                cur.execute("insert into t_scm_config (CODE, VALUE, USERID, TENANTID) values ('one_step_certify', '1', null, '999999999')")
            else:
                cur.execute("insert into t_scm_config (CODE, VALUE, USERID, TENANTID) values ('one_step_certify', '0', null, '999999999')")
        else:
            if flag == "1":
                cur.execute("update t_scm_config set value=1 where tenantid = '" + tenant + "' and code = 'one_step_certify'")
            else:
                cur.execute("update t_scm_config set value=0 where tenantid = '" + tenant + "' and code = 'one_step_certify'")
        conn.commit()
        cur.close()
        conn.close()
        return "52 server onstep is " + flag + " init ok!"
    else:
        return "db error"

    cursor = conn.cursor()

    result_of_select_step = select_on_step(tenant)
    if result_of_select_step is None:
        insert_one_step(tenant, flag)
    else:
        update_one_step(tenant, flag)
    result_of_select_step = select_on_step(tenant)
    cursor.close()
    conn.close()
    if result_of_select_step[0] == "1":
        return "oneStep set OK"
    else:
        return "not oneStep set OK"


@app.route('/taxperiod')
def taxperiod():
    taxno = request.args.get("taxno")
    op = request.args.get("op")
    db = request.args.get("db")
    select_period_sql = "select 1 from t_scm_taxno_info WHERE taxno='" + taxno + "'"
    del_period_sql = "DELETE FROM t_scm_taxno_info WHERE taxno='" + taxno + "'"
    update_period_sql = "update `t_scm_taxno_info` t set income_month=NULL where t.taxno='" + taxno + "'"
    if db == "223":
        pass
        #conn = cx_Oracle.connect('jxstanded/jxstanded@192.168.0.245:1521/csdb')  # 1个参数
    elif db == "16":
        pass
        #conn = cx_Oracle.connect('bxjx/bxjx@192.168.7.170:1521/orcl')  # 1个参数
    elif db == "52":
        conn = pymysql.connect(host='192.168.6.62', user='root', passwd='baijia*58', db='jxstanded', port=3306, charset='utf8')
    else:
        return "db not exist"
    cur = conn.cursor()
    cur.execute(select_period_sql)

    if op == "del":
        if cur.fetchone() is not None:
            print(del_period_sql)
            cur.execute(del_period_sql)
        else:
            return db + " taxperiod does not exist,no need to del"
    elif op == "null":
        if cur.fetchone() is not None:
            print(update_period_sql)
            cur.execute(update_period_sql)
        else:
            return db + " taxperiod does not exist,can not set null"
    else:
        return "op must = :[del | null]"
    cur.close()
    conn.commit()
    conn.close()
    return db + " taxperiod " + op + " ok"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
