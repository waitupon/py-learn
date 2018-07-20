#!/usr/bin/python3
# coding=gbk

import pymysql

# 打开数据库连接
db = pymysql.connect(host="192.168.6.14",port=3306, user="xiang", passwd="nEw-TESt@&2#", db="two_invoice_check",charset='utf8')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 查询语句


try:

    for num in range(10,200):
         invkind = "123" + str(num)
         invNum = "123" + str(num)
       #  sql = "INSERT INTO `two_invoice_check`.`t_scm_vat_main` ( `BUYER_TAXNO`, `INV_KIND`, `INV_NUM`, `SELLER_TAXNO`, `INV_DATE`, `INV_COST`, `INV_VAT`, `INV_SUM`, `INV_RATE`, `INV_PWD`, `INV_DEDU_RESULT`, `INV_TYPE`, `INV_FROM`, `INV_STATUS`, `SCAN_MATCH`, `MATCH_STATUS`, `INV_TAX_SIGN`, `INV_COMMENT`, `INV_ERR_INFO`, `INV_DEDU_DATE`, `INV_CONFIRM_DATE`, `INV_CONFIRM_USER`, `INV_SEND_TIME`, `INV_RECE_TIME`, `SCAN_DATE`, `SCAN_USER`, `SCAN_NO`, `INV_INPUT_USER`, `INV_INPUT_TIME`, `INV_DRAW_TIME`, `INV_SCAN_TIME`, `BUYER_NAME`, `BUYER_ADDR_TEL`, `BUYER_BANK`, `SELLER_NAME`, `SELLER_ADDR_TEL`, `SELLER_BANK`, `MATCH_NO`, `MATCH_DATE`, `MATCH_USER`, `MATCH_ERR_INFO`, `SELLER_ID`, `PO_IDS`, `PO_TYPE`, `INV_TAXNO`, `SCAN_BATCH`, `CHGRES_USER`, `CHGRES_TIME`, `ERR_UPDATE_TIME`, `IS_TRANS`, `MATCH_COST`, `MATCH_VAT`, `FULL_CODE`, `FLOW_STATUS`, `CREATE_DATE`, `CREATE_BY`, `UPDATE_DATE`, `UPDATE_BY`, `INCOME_MONTH`, `RECORD_MONTH`, `INV_CONFIRM_STATUS`, `IMG_PATH`, `IMG_TIME`, `IS_COLLECT_ALL`, `COLLECT_TIME`, `IS_SCANNER`, `DEDU_INFO`, `UPDATE_DEDU_INFO_DATE`, `RECEV_FLAG`, `SCAN_UPDATE_DATE`, `SYS_COMPANY_CODE`, `SYNC_TASKNO`, `SYNC_SEND_STATUS`, `SIGN_TASKNO`, `SIGN_SEND_STATUS`, `DEDU_TASKNO`, `DEDU_SEND_STATUS`, `DEDU_APPLY_TASKNO`, `SYS_ORG_CODE`, `CHECK_TIME`, `RECEV_WAY`, `IS_TAXNO_FILL`, `APPLY_CONFIRM_TASKNO`, `CHECK_CODE`, `MACHINE_CODE`, `RECEIVING_CLERK`, `TOTAL_AMOUNT_CN`, `FULL_BUYER_TAXNO`, `PRE_DEDUCT_FLAG`, `TOLLSIGN`, `ZEROTAXRATESIGN`, `CHECK_ERR_CODE`, `IS_SAME_TAXINFO`, `ACCOUNT_TIME`, `VOUCHER_NUM`, `CERTIFICATION_WAY`, `CERTIFICATION_TYPE`, `IS_AGENCY_REBATE`, `peers_match_no`, `drug_approved_no`, `drug_produce_no`, `validity_period`, `pre_inv_num`, `remain_count`, `gnum_count`, `peers_match_status`) VALUES ('565401010160gd8047', '"+invkind+"', '"+invNum+"', '911201163409833307', '2017-12-02', '203.88', '6.12', '210.00', '0.03', NULL, '0', '04', '3', '0', '1', '1', '0', NULL, NULL, '2018-03-30 19:34:25', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '百望股份有限公司', NULL, NULL, '滴滴出行科技有限公司', '天津经济技术开发区南港工业区综合服务区办公楼C座103室12单元022-59002850', '招商银行股份有限公司天津自由贸易试验区分行122905939910401', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2018-07-09 16:00:01', 'systemauto', '201801', NULL, '0', NULL, NULL, '1', NULL, '2', NULL, NULL, NULL, NULL, '1000', '14279-20180619112636', NULL, NULL, NULL, NULL, NULL, NULL, '1000000000672', '2018-03-30 15:49:22', NULL, NULL, NULL, '01609085326666425995', '499099606269', NULL, '肆拾柒圆贰角肆分', NULL, '1', NULL, NULL, '101', '1', NULL, NULL, NULL, NULL, NULL, NULL, 'Z20025338', '1709014', '2018-07-05', '2018060301-0341', '0.00', '6.00', NULL)";
         sql = "INSERT INTO `two_invoice_check`.`t_scm_done_vat_main` (`pre_inv_num`, `inv_type`, `buyer_name`, `buyer_taxno`, `seller_taxno`, `seller_name`, `inv_cost`, `inv_vat`, `inv_sum`, `remarks`, `reviewer_name`, `payee_name`, `billing_name`, `inventory_mark`, `pre_date`, `print_status`, `settle_no`, `inv_kind`, `inv_num`, `apply_no`, `inv_date`, `invpwd`, `check_code`, `invoice_qr_code`, `update_date`, `update_by`, `buy_email`, `buy_phone`, `source_marker`, `taxation_mode`, `deductible_amount`, `open_inv_type`, `inv_state`, `device_type`, `serial_no`, `invoice_terminal_code`, `invoice_special_mark`, `seller_address_phone`, `buyer_address_phone`, `tax_control_code`, `format_file_url`, `invoice_invalid_reason`, `invoice_invalid_operator`, `invoice_invalid_date`, `invoice_status`, `invoice_upload_mark`, `invoice_sign_mark`, `invoice_check_mark`, `organization_id`, `tenant_id`, `redInfo_no`, `original_invoice_code`, `original_invoice_no`, `consolidated_tax_rate`, `notification_no`, `signature_parameter`, `goods_code_version`, `create_by`, `create_date`, `seller_bank_account`, `buyer_bank_account`, `synch_state`, `failure_reason`, `format_file_status`, `format_file_time`, `machine_code`, `peers_match_no`, `sign_status`, `sign_date`, `sign_user`, `match_status`, `peer_goods_count`, `sys_org_code`, `not_match_gnum`, `gnum_count`, `ship_species`, `sys_company_code`) VALUES ('121312-3240011', '2', '3', '5654010101668d8047', '565401010160gd8047', '百望股份有限公司', '7.00', '8.00', '9.00', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '"+invkind+"', '"+invNum+"', NULL, '2018-07-05', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '22', 'N', 'N', 'N', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '0', NULL, '0', NULL, NULL, NULL, '2', '2018-07-16 13:50:07', '租户管理员', '0', '12', '1000000000672', '1.00', NULL, '12', NULL)";
         #preInvNum = "121312-3240011" + str(num)
        # sql = "INSERT INTO `two_invoice_check`.`t_scm_peers_goods` ( `goods_no`, `buyer_name`, `inv_type`, `billing_name`, `payee_name`, `reviewer_name`, `remarks`, `peers_match_no`, `sign_status`, `sign_date`, `sign_user`, `inv_state`, `is_merge`, `merge_no`, `merge_date`, `merge_user`, `match_status`, `create_date`, `create_by`, `update_date`, `update_by`, `ship_date`, `not_match_count`, `ship_cost`, `distribution_address`, `ship_user`, `buyer_taxno`, `seller_taxno`, `seller_name`, `ship_species`, `sys_org_code`, `gnum_count`, `uploader`, `serial_no`, `inv_cost`, `inv_sum`, `inv_vat`, `print_status`, `sys_company_code`) VALUES ('"+preInvNum+"', '门源县第一人民医院', '007', '张三', '李四', '王五', '备注', NULL, '2', '2018-07-14 21:45:22', '租户管理员', '0', '0', NULL, NULL, NULL, '3', '2018-06-27 14:06:43', 'lts01', NULL, NULL, '2018-06-23 00:00:00', '2', '350.00', '北京马连洼', '李六', '5654010101668d8047', '501234567890000118', '海尔股份1', '2', '1000000000672', '10.00', NULL, NULL, '339.80', '350.00', '10.20', '0', NULL);";
         # 执行SQL语句
         cursor.execute(sql)
         db.commit()


except:
    print("Error: unable to fetch data")

# 关闭数据库连接
db.close()