# realtime data streaming from API


# Table of contents
<!-- vscode-markdown-toc -->
* I. [Introduction](#I.Introduction)
	* 1.1 [Overview](#Overview)
	* 1.2 [The goal of this project](#Thegoalofthisproject)
	* 1.3 [Prerequisites](#Prerequisites)
	* 1.4 [Dependencies](#Dependencies)
	* 1.5 [Data sources](#Datasources)
* II. [Architecture](#II.Architecture)
* III. [How It Works](#III.HowItWorks)
* IV. [Usage](#IV.Usage)
	updating
* V. [Demo]
	updateing

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->


##  <a name='I.Introduction'></a>I. Introduction
    
###  1.1 <a name='Overview'></a>Overview
This project aims to develop a real-time data streaming system for processing and analyzing data from various sources, including APIs, sensors, and cameras. The system utilizes a robust architecture, leveraging technologies like Docker, Django, Kafka, Spark, and Cassandra to ensure efficient data ingestion, processing, and storage.

###  1.2 <a name='Thegoalofthisproject'></a>The goal of this project
The primary objectives of this project are:
- Establish a scalable and reliable infrastructure for real-time data streaming.
- Implement effective data processing and analysis pipelines.
- Provide valuable insights and visualizations based on the processed data.

###  1.3 <a name='Prerequisites'></a>Prerequisites
Before proceeding, ensure you have the following prerequisites in place:
- A Docker environment (Docker Desktop or similar).
- Python 3.x installed.
- Basic knowledge of Python programming.
- Familiarity with data streaming concepts.
- Understanding of cloud-based infrastructure (optional).
- Other libraries and tools as specified in the `requirements.txt` file.

###  1.4 <a name='Dependencies'></a>Dependencies
The project relies on the following dependencies:
- Django
- Kafka
- Spark
- Cassandra
- Docker
- Other libraries and tools as specified in the `requirements.txt` file.

###  1.5 <a name='Datasources'></a>Data sources
The system can ingest data from various sources, including:
- APIs (https://randomuser.me/)
- Sensors (e.g., temperature, humidity, pressure)
- Cameras (e.g., surveillance footage)
- Other real-time data streams

## <a name='II.Architecture'></a>II. Architecture

<img src="./system_architecture.png"/> 
<br />

The system architecture is illustrated in the provided diagram. Key components include:
- **Data Sources:** Generate real-time data streams.
- **Kafka:** A distributed streaming platform for ingesting and processing data.
  - Includes components like **Zoomkeeper** and **Control Center** for monitoring and managing the Kafka environment.
  - Utilizes a **Schema Registry** to manage schemas for data consistency.
- **Django:** A web framework for building the user interface and handling API requests.
  - Acts as a Kafka consumer that receives data for real-time model training and results delivery to the client (HTML, CSS, JS).
- **Spark:** A powerful big data processing engine for analyzing and transforming data.
  - Processes data from Kafka for big data analysis and stores results in **Cassandra**.
- **Cassandra:** A NoSQL database for storing and querying large datasets.
- **Docker:** A containerization platform for packaging and deploying applications.

## <a name='III.HowItWorks'></a>III. How It Works

1. **Data Ingestion:** 
   - Data is sourced from APIs (e.g., randomuser.me) and sent to Kafka for real-time processing.
  
2. **Data Processing:** 
   - Kafka distributes the data to two paths:
     - **Path 1:** Data is sent to Spark for big data processing. Spark applies transformations and analysis techniques, and the results are stored in Cassandra.
     - **Path 2:** The Django server acts as a Kafka consumer, receiving data from Kafka. It trains a model in real-time using this data and also retrieves data from Cassandra to enhance the training process.

3. **Model Training:**
   - The trained model results are stored as a pickle file for future use by the Django server, allowing for quick predictions and responses.

4. **Data Storage:** 
   - Processed data and model outputs are stored in Cassandra for future reference and analysis.

5. **Visualization:** 
   - Django serves as the frontend, providing a user interface to visualize and interact with the processed data and model predictions.

## <a name='IV.Usage'></a>IV. Usage
