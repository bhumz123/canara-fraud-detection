# Canara-Fraud-Detection

Our ultimate objective is to develop a real-time Data Analytics based fraud detection model based fraud detection model that effectively detects fraud while minimizing false positives and negatives. To achieve this, we employ technologies such as Flask API, Kafka streaming, and PostgreSQL for efficient data processing and storage. Our focus is to maintain a shorter streaming time while ensuring accurate fraud detection and reducing financial risks.

# Project Setup Guide

## Cloning the GitHub Repository

Follow these steps to clone the GitHub repository:

1. **Navigate to the Repository:**
   - Open a web browser and go to the GitHub repository [Canara Fraud Detection](https://github.com/bhumz123/canara-fraud-detection).

2. **Copy Repository URL:**
   - Locate the "Clone or download" button and click the "Copy URL" option. This will copy the repository's URL to your clipboard.
3. **Open Terminal:**
   - Launch a terminal window on your local machine.

4. **Change Directory:**
   - Use the `cd` command to navigate to the directory where you want to clone the repository.

5. **Clone Repository:**
   - Use the `git clone` command followed by the copied repository URL.

```git clone https://github.com/bhumz123/canara-fraud-detection.git ```


## For the installation and setup of kafka follow the commands given below :-

``` .\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties 
.\bin\windows\kafka-server-start.bat .\config\server.properties ```
bin\windows\kafka-topics.bat --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3 --topic testc

bin\windows\kafka-console-producer.bat --bootstrap-server localhost:9092 --topic testc
bin\windows\kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic testc --from-beginning 
```


## For the installation of PostGresSQL follow the steps given below :-

1.  **Download PostGresSQL , and open PgAdmin4.**

2. **Create a database and name it test_db.**


## Execution of the PROJECT:-

Follow the given order of files for the successful execution of the project.

1. **fraudpredictions_api.py**
2. **test_data_producer.py**
3. **test_kafka_consumer.py**

