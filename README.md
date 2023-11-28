# canara-fraud-detection


Our ultimate objective is to develop a real-time Data Analytics based fraud detection model based fraud detection model that effectively detects fraud while minimizing false positives and negatives. To achieve this, we employ technologies such as Flask API, Kafka streaming, and PostgreSQL for efficient data processing and storage. Our focus is to maintain a shorter streaming time while ensuring accurate fraud detection and reducing financial risks.

# Steps to clone the github repository-


Navigate to the Repository: Open a web browser and go to the GitHub repository https://github.com/bhumz123/canara-fraud-detection
Copy Repository URL: Locate the "Clone or download" button and click the "Copy URL" option. This will copy the repository's URL to your clipboard.
Open Terminal: Launch a terminal window on your local machine.
Change Directory: Use the cd command to navigate to the directory where you want to clone the repository.
Clone Repository: Use the git clone command followed by the copied repository URL. 


# For the installation and setup of kafka follow the commands given below :-


1) .\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties

2) .\bin\windows\kafka-server-start.bat .\config\server.properties

3) bin\windows\kafka-topics.bat --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3 --topic testc

4) bin\windows\kafka-console-producer.bat --bootstrap-server localhost:9092 --topic testc

5) bin\windows\kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic testc --from-beginning




# For the installation of PostGresSQL follow the steps given below :-

1) Download PostGresSQL , and open PgAdmin4.

2) Create a database and name it test_db.


# Execution of the PROJECT:-

Follow the given order of files for the successful execution of the project.

1) fraudpredictions_api.py
2) test_data_producer.py
3) test_kafka_consumer.py

# Please follow the steps outlined below:
# GitHub Repository:
 All project-related files, code, and documentation are available on our GitHub repository.
#Detailed Instructions:
Comprehensive instructions for setting up and running the project are provided within the GitHub repository.
Navigate to the root directory of the repository and refer to the 'README.md' file for step-by-step guidance.
# Large File Considerations:
- Due to the substantial size of some project files, we were unable to upload them directly to GitHub (which has a file size limit of 1GB).
- Instead, we have provided Google Drive links at designated locations within the repository where these larger files can be downloaded locally.
Utilizing Original Models:
#  For execution purposes, it is essential to download and utilize the original models and files available through the provided Google Drive links.
# Execution of the project:-
# Follow the given order of files for the successful execution of the project.
1) fraudpredictions_api.py
2) test_data_producer.py
3) test_kafka_consumer.py
