from pyspark.sql import SparkSession

master = 'local'

spark = SparkSession.builder.appName('test').master(master).getOrCreate()

sc = spark.sparkContext
filename = 'file:///home/pyspider/derby.log'
logData = sc.textFile(filename)
wordsRDD = logData.flatMap(lambda x: x.split(" ")).map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y)

out_filename = 'result'
wordsRDD.saveAsTestFile(out_filename)
words = wordsRDD.collect()
spark.stop()
