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
* IV. [Usage](#iv-usage)
* V. [Demo](#v-demo)

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
### Step-by-Step Setup Guide

1. **Install Visual Studio Code**  
   Download and install Visual Studio Code from [here](https://code.visualstudio.com/download).

2. **Install Python 3**  
   Download and install Python 3 from [here](https://www.python.org/downloads/).

3. **Install Docker**  
   - Download Docker Desktop from [here](https://www.docker.com/products/docker-desktop).
   - Install Docker Engine by following the instructions [here](https://docs.docker.com/engine/install/).

4. **Install Git**  
   Download and install Git from [here](https://github.com/git-guides/install-git).

5. **Clone the Repository**
   - Open your terminal and clone the project repository:
     ```bash
     git clone https://github.com/HuyPham103code/realtime_data_streamming.git
     ```
   - Navigate into the project directory:
     ```bash
     cd realtime_data_streamming
     ```

6. **Set Up the Virtual Environment**
   - Create a virtual environment:
     ```bash
     py -m venv venv
     ```

7. **Open the Project in Visual Studio Code**
   - Open the `realtime_data_streamming` folder in Visual Studio Code.
   - Activate the virtual environment:
     ```bash
     .\venv\Scripts\activate
     ```

8. **Install Extensions and Packages**
   - Install the **Live Server** extension in Visual Studio Code for serving static files.
   - Install the necessary Python packages:
     ```bash
     pip install cassandra-driver pandas
     ```

9. **Run Docker Containers**
   - Start Docker containers:
     ```bash
     docker compose up -d
     ```
   - To stop the Docker containers, use:
     ```bash
     docker compose down
     ```

10. **Connect to Cassandra**
    - Access the Cassandra shell using:
      ```bash
      docker exec -it cassandra cqlsh -u cassandra -p cassandra localhost 9042
      ```

11. **Verify Data in Cassandra**
    - Run the following query to confirm data ingestion in Cassandra:
      ```cql
      SELECT * FROM spark_streams.created_users;
      ```

## V. Demo
[Click here to watch the demo video](video_demo.mp4) 

