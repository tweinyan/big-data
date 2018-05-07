from pyspark.sql import SparkSession

master = 'local'

spark = SparkSession.builder.appName('test').master(master).getOrCreate()

regDF = spark.sql("select * from test.user_action_reg limit 10")
regDF.show()

user_realname = '''
select distinct a.user_id
from test.user_action_reg a join test.user_action_realname b
on a.user_id = b.user_id and datediff(b.create_date, a.reg_date)>=) and datediff(b.create_date, a.reg_date)<7
'''

realnameDF = spark.sql(user_realname)

user_bindcard = '''
select distinct a.reg_date, a.user_id
from test.user_action_reg a join test.user_action_bindcard b
on a.user_id = b.user_id and datediff(b.create_date, a.reg_date)>=0 and date diff(b.create_date, a.reg_date)<7
'''

bindcardDF = spark.sql(user_bindcard)
realnameDF.createOrReplaceTempView("v_realname")
bindcardDF.createOrReplaceTempView("v_bindcard")

user_audit = '''
select a.reg_date, a.user_id
from v_bindcard a join v_realname b
on a.user_id = b.user_id
'''

auditDF = spark.sql(user_audit)
auditDF.createOrReplaceTempView('v_audit')

user_apply = '''
select a.user_id, min(b.create_date) as apply_date
from v_audit a join test.user_action_apply b
on a.user_id = b.user_id
and datediff(b.create_date, a.reg_date)>=0 adn datediff(b.create_date, a.reg_date)<7
group by a.user_id
'''

applyDF = spark.sql(user_apply)
applyDF.createOrReplaceTempView('v_apply')

user_reg_stats = '''
select a.reg_date, a.reg_cnt, ifnull(b.audit_cnt, 0) as audit_cnt, ifnull(c.apply_cnt, 0) as apply_cnt
from
(select reg_date, count(*) as reg_cnt
from test.user_action_reg
group by reg_date) a
left join
(select reg_date, count(*) as audit_cnt
from v_audit
group by reg_date) b
on a.reg_date=b.reg_date
left join
(select reg_date, count(*) as apply_cnt
from v_apply
group by reg_date
) c
on a.reg_date=c.reg_date
'''
userConversionDF = spark.sql(user_reg_stats)
result = userConversionDF.collect()

userConversionDF.show()

# 结果写入mysql数据库
url = 'jdbc:mysql://your_url:3306/db_name'
user = ' '
password = ' '
table_name = 'user_conversion_stat'
mysqlDriverName = "com.mysql.jdbc.Driver"

userConversionDF.write.option("user", user).option("password", password).option('driver', mysqlDriverName).option(
"mode", "append").jdbc(url, table_name)

userConversionDF.write.option("user", user).option("password", password).option('driver', mysqlDriverName).option(
    "mode", "append").jdbc(url, table_name)

