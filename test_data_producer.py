import json
import time
import pandas as pd
import requests
from observability import logger_provider, logger

URL = 'http://127.0.0.1:5001/canara/stream/send_event'


def load_data():
    data = pd.read_csv(filepath_or_buffer="Test__Dataset.csv", nrows=16)
    json_data = data.to_dict('records')
    for record in json_data:
        # print(record)
        start_time = time.time()
        response = requests.post(url=URL, json=record)
        msg = f"Getting response from api- Status Code: {response.status_code} and data: {response.json()}"
        logger.info(msg)
        print(msg)
        end_time = time.time()
        process_time = end_time - start_time
        msg = "process took {0} ms".format(process_time * 10 ** 3)
        logger.info(msg)
        print(msg)
        time.sleep(1)


if __name__ == "__main__":
    load_data()
    logger_provider.shutdown()
