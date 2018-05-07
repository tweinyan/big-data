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

df.withColumn('newWidth', df.SepalWidth * 2).show()

# ==================== 删除一列 drop ====================
df.drop('Name').show()

# ==================== 统计信息 describe ====================
df.describe().show()
df.describe('Name').show()   # 分类变量

# ==================== 提取部分列 select ====================
df.select('Name', 'SepalLength').show()

# ==================== 过滤行 filter ====================

import pyspark.sql.functions as fun

estDF2 = testDF.withColumn('New_name', check(testDF['Name'])).filter('New_name <> -1')
testDF.withColumn('New_name', check(testDF['Name'])).filter(fun.col('Name')<>-1).show()

# ==================== 基本统计功能 distinct count ====================
df.select('Name').distinct().count()

# 分组统计 groupby(colname).agg({'col':'fun', 'col2': 'fun2'})
df.groupby('Name').agg({'SepalWidth': 'mean', 'SepalLength': 'max'}).show()

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
