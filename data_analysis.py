import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

from pyspark.sql import SparkSession, functions, types
spark = SparkSession.builder.appName('read stream').getOrCreate()
assert spark.version >= '3.0' # make sure we have Spark 3.0+
spark.sparkContext.setLogLevel('WARN')


# Read data from Clickhouse and 
def read_data():
    ...


# Calculate hurst exponent for each time series to determine if it has momentum or stationarity
def hurst_exponent():
    ...


# Detect volume spikes for potential incoming momentum in price changes
def spike_detection():
    ...


# Find out types of coins trending
def sector_hotness():
    ...


def output_result():
    ...

