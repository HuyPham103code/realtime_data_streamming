#!/bin/bash

# Đợi 120 giây trước khi khởi động Spark Streaming
sleep 120

# Chạy Spark Streaming
spark-submit --master spark://spark-master:7077 spark_streams.py
