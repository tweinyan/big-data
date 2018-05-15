from pyspark import SparkContext
from pyspark.streaming import StreamingContext

def get_countryname(line):
    country_name = line.strip()

    if country_name == 'usa':
        output = 'USA'
    elif country_name == 'ind':
        output = 'India'
    elif country_name == 'aus':
        output = 'Australia'
    else:
        output = 'Unknown'
    return (output, 1)

if __name__ == "__main__":
    batch_interval = 1
    window_length = 6 * batch_interval
    frequency = 3 * batch_interval

    spc = SparkContext(appName="windowCount")
    stc = StreamingContext(spc, batch_interval)
    stc.checkpoint("checkpoint")

    lines = stc.socketTextStream('localhost', 9999)
    addFunc = lambda x, y: x + y
    invAddFunc = lambda x, y: x - y
    window_counts = lines.map(get_countryname) \
        .reduceByKeyAndWindow(addFunc, invAddFunc, window_length, frequency)

    window_counts.pprint()

    stc.start()
    stc.awaitTermination()
