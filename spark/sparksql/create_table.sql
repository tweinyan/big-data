==================== 用户注册 ==================== 
drop table if exists test.user_action_reg;

CREATE EXTERNAL TABLE test.user_action_reg(
    surr_data_id int,
    user_id int,
    phone string,
    reg_date date,
    idcard string,
    platform string,
    user_product_line string,
    user_promotion_channel string,
    source string,
    promo_action_id int
) ROW FORMAT SERDE
    'org.apache.hadoop.hive.serde2.lazySimpleSerDe'
WITH SERDEPROPERTIES (
    'field.delim'=',',
    'line.delim'='\n',
    "serialization.encoding"='GBK'
) 
STORED AS INPUTFORMAT
    'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
    'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
    'hdfs:///tmp/zxm/uc/reg'
;
select * from test.user action_reg_limit 10;

==================== 用户实名认证 ==================== 
drop table if exists test.user_action_realname;

CREATE EXTERNAL TABLE test.user_action_realname(
    id int,
    user_id int,
    gender string,
    birthday string,
    address string,
    card_org string,
    valid_date string,
    create_date date,
    nation string
)
ROW FORMAT SERDE
    'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
    'field.delim'=',',
    'line.delim'='\n',
    'serialization.format'=',',
    "serialization.encoding"='GBK'
)
STORED AS INPUTFORMAT
    'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
    'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
    'hdfs:///tmp/zxm/uc/realname'
;

select * from test.user_action_realname limit 10;

-- 七日内完成实名认证
select distinct a.user_id
from test.user_action_reg a join test.user_action_realname b
on a.user_id = b.user_id and datediff(b.create_date, a.reg_date)>=0 and datediff(b.create_date, a.reg_date)<7

==================== 用户绑定银行卡 ====================
drop table if exists test.user_action_bindcard;
CREATE EXTERNAL TABLE test.user_action_bindcard(
    id int,
    user_id int,
    bank_name string,
    branch_bank string,
    bank_province_id int,
    bank_city_id int,
    bank_area_id int,
    bank_num string,
    bank_phone string,
    repay_status int,
    create_date date,
    update_time string,
    pay_type int
)
ROW FORMAT SERDE
    'org.apache.hadoop.hive.sesrde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
    'field.delim'=',',
    'line.delim'='\n'
    'serialization.format'=',',
    "serialization.encoding"='GBK'
)
STORED AS INPUTFORMAT
    'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
    'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
    'hdfs:///tmp/zxm/uc/bankcard'
;

select * from test.user_action_bindcard limit 10;
-- 七日内完成绑卡认证
select distinct a.reg_date, a.user_id
from test.user_action_reg a join test.user_action_bindcard b
on a.user_id = b.user_id and datediff(b.create_date, a.reg_date)>=0 and date diff(b.create_date, a.reg_date)<7
-- 七日内完成认证(包括实名和绑卡)
select a.reg_date, a.user_id
from v_bindcard a join v_realname b
on a.user_id = b.user_id
