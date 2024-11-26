"""
Input Pyspark Dataframe for live data feed and whichever historical data needed from Clickhouse Database
Output Pyspark Dataframe for aggregated results to Grafana for visualization
"""


import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

from pyspark.sql import SparkSession, functions, types
spark = SparkSession.builder.appName('read stream').getOrCreate()
assert spark.version >= '3.0' # make sure we have Spark 3.0+
spark.sparkContext.setLogLevel('WARN')


# Read data from Clickhouse and 
def read_data(inputs):
    ...


# Calculate hurst exponent for each time series to determine if it has momentum or stationarity
def hurst_exponent(df, rolling_window=25):
    ...


# Detect volume spikes for potential incoming momentum in price changes
def spike_detection(df, rolling_window=100):
    ...


# Find out types of coins trending
def sector_hotness(df, rolling_window=25):
    ...


def output_result(df):
    ...

