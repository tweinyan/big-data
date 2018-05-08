# ==================== 直接创建DataFrame
from pyspark.sql import SparkSession
from pyspark.sql import Row

spark = SparkSession.builder.appName('test').getOrCreate()
sc = spark.sparkContext

# ==================== 直接创建 ====================

l = [('Ankit', 25), ('Jalfaizy', 22), ('saurabh', 20), ('Bala', 26)]
rdd = sc.parallelize(l)

people = rdd.map(lambda x: Row(name=x[0], age=int(x[1])))
schemaPeople = spark.createDataFrame(people)

# ==================== 从csv读取 ====================
df = spark.read.format("csv"). \
    option("header", "true"). \
    load("iris.csv")

df.printSchema()
df.show(10)

df.count()
df.columns

# ==================== 增加一列(或者替换)
# withColumn====================
# Column name which we want add /replace
# Expression on column

df.withColumn('newWidth', df.sepal_width * 2).show()

# ==================== 删除一列 drop ====================
df.drop('species').show()

# ==================== 统计信息 describe ====================
df.describe().show()
df.describe('species').show()   # 分类变量

# ==================== 提取部分列 select ====================
df.select('species', 'sepal_length').show()

# ==================== 基本统计功能 distinct count ====================
df.select('species').distinct().count()

# 分组统计 groupby(colname).agg({'col':'fun', 'col2': 'fun2'})
df.groupby('species').agg({'sepal_width': 'mean', 'sepal_length': 'max'}).show()

# avg(), count(), countDistinct(), first(), kurtosis(),
# max(), mean(), min(), skewness(), stddev(), stddev_pop(),
# stddev_samp(), sum(), suimDistinct(), var_pop(), var_same() and
# variance()


# 自定义的汇总方法

import pyspark.sql.functions as fn

df.agg(fn.count('id').alias('id_count'), fn.countDistinct('id').alias('distinct_id_count')).collect()

# ==================== 数据集拆分成两部分 randomSplit ====================
trainDF, testDF = df.randomSplit([0.6, 0.4])



# ==================== 采样数据 sample ====================
# withReplacement = True or False to select a observation with or without
# replacement.
# fraction = x, where x = .5 shows that we want to have 50% data in sample
# DataFrame.
# seed for reproduce the result
sdf = df.sample(False, 0.2, 100)

# 查看两个数据集在类别上的差异 subtract, 确保训练数据覆盖了所有分类

diff_in_train_test = testDF.select('species').subtract(trainDF.select('species'))
diff_in_train_test.distinct().count()

# ==================== 交叉表 crosstab ====================
df.crosstab('species', 'sepal_length').show()


# ==================== sql 功能 ====================
df.registerAsTable('train_table')
spark.sql("").show()

# ==================== 综合案例， + udf ====================
# 测试数据集中有些类别在训练集中是不存在，把这些数据集应该从测试集中删除
trainDF, testDF = df.randomSplit([0.01, 0.98])

diff_in_train_test = testDF.select('species').subtract(trainDF.select('species')).distinct().show()

# 首先找到这些类，整理到一个列表
not_exist_cats = testDF.select('species').subtract(trainDF.select('species')).distinct().rdd.map(lambda x: x[0]).collect()


# 定义一个方法，用于检测
def should_remove(x):
    if x in not_exist_cats:
        return -1
    else:
        return x

# 创建udf, udf函数需要两个从参数：
# Function
# Return type (in my case StringType())

from pyspark.sql.types import StringType
from pyspark.sql.functions import udf

check = udf(should_remove, StringType())

testDF2 = testDF.withColumn('New_name', check(testDF['species'])).filter("New_name <> '-1'")

testDF2.show()

# ==================== 过滤行 filter ====================
import pyspark.sql.functions as fun

testDFF2 = df.withColumn('New_name', check(testDF['Name'])).filter("New_name <> -1")
df.withColumn('New_name', check(testDF['Name'])).filter(fun.col('Name')<>-1).show()

