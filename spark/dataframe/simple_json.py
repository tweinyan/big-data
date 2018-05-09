from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('json_demo').getOrCreate()
sc = spark.sparkContext

# ==================================================
#                 无嵌套结构的json
# ==================================================
jsonString = [
"""{ "id" : "01001", "city" : "AGAWAM",  "pop" : 15338, "state" : "MA" }""",
"""{ "id" : "01002", "city" : "CUSHMAN", "pop" : 36963, "state" : "MA" }"""
]

# 从json字符串数组得到rdd有两种方法
# 1. 转换为rdd, 再从rdd到DataFrame
# 2. 直接利用spark.createDataFrame(), 见后面例子

zipJSONRDD = sc.parallelize(jsonString)

zipJSONDF = spark.read.json(zipJSONRDD)

zipJSONDF.printSchema()
zipJSONDF.show()
zipJSONDF.collect()
zipJSONDF.take(2)

# 直接从文件生成DataFrame

jsonDF = spark.read.json("zips.json")

jsonDF.printSchema()
jsonDF.show()

jsonDF.filter(jsonDF.pop>4000).show(10)
# 注册为临时表
jsonDF.createOrReplaceTempView("zips_table")
resultDF = spark.sql("select * from zips_table where pop>4000")
resultDF.show(10)

#
# ==================================================
# 2.如何指定DataFrame的schema
#   有两种方法1: 通过反射自动推断, 2：程序指定
#   前一种方法适合静态数据
#   后一种方法非常适合程序运行中动态生成的数据
#
#   前面例子pop被当字符串对待，显然是不正确的

'''
    1. 没有嵌套结构的json
'''
jsonString = [
"""{ "id" : "01001", "city" : "AGAWAM",  "pop" : 15338, "state" : "MA" }""",
"""{ "id" : "01002", "city" : "CUSHMAN", "pop" : 36963, "state" : "MA" }"""
]

zipJSONRDD = sc.parallelize(jsonString)

from pyspark.sql.types import *

jsonSchema = StructType() \
    .add("id", StringType(), True) \
    .add("city", StringType()) \
    .add("pop", LongType()) \
    .add("state", StringType())

reader = spark.read
reader.schema(jsonSchema)

zipJSONDF = reader.json(zipJSONRDD)
zipJSONDF.printSchema()
zipJSONDF.show()

'''
    2.带有嵌套结构的schema
    方法1
'''
from pyspark.sql.types import *
jsonSchema = StructType([
    StructField("_id", StringType(), True),
    StructField("city", StringType(), True),
    StructField("loc", ArrayType(DoubleType())),
    StructField("pop", LongType(), True),
    StructField("state", StringType(), True),
])

reader = spark.read
reader.schema(jsonSchema)
jsonDF = reader.json('zips.json')
jsonDF.printSchema()
jsonDF.show(2)
jsonDF.filter(jsonDF.pop>4000).show(10)

'''
    方法2
jsonSchema = StructType() \
    .add("id", StringType(), True) \
    .add("city", StringType()) \
    .add("pop", LongType()) \
    .add("state", StringType()) \
    .add("loc", StructType().add("lat", DoubleType()).add(
    "long", DoubleType()))
'''


