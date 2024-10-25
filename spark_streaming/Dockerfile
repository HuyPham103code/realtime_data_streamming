# # Dockerfile
# FROM bitnami/spark:latest

# # Copy the Python script into the container
# COPY spark_streams.py /app/spark_streams.py

# # Install necessary Python packages
# RUN pip install cassandra-driver spark pyspark

# # Set the working directory
# WORKDIR /app

# # Create a start.sh script to sleep for 2 minutes and then run the Spark job
# RUN echo '#!/bin/sh\nsleep 120\nspark-submit --master spark://spark-master:7077 spark_streams.py' > start.sh

# # Make the start.sh script executable
# RUN chmod +x start.sh

# # Command to run the start script
# CMD ["./start.sh"]



# Dockerfile
FROM bitnami/spark:latest

# Set the working directory
WORKDIR /app

# Copy the Python script into the container
COPY spark_streams.py /app/spark_streams.py

# Install necessary Python packages
RUN pip install cassandra-driver spark pyspark

CMD ["sh", "-c", "sleep 60 && python spark_streams.py"]

# # Create a start.sh script to sleep for 2 minutes and then run the Spark job
# RUN sh -c 'echo "#!/bin/sh\nsleep 120\nspark-submit --master spark://spark-master:7077 spark_streams.py" > start.sh'

# # Make the start.sh script executable
# RUN chmod +x start.sh

# # Command to run the start script
# CMD ["./start.sh"]
