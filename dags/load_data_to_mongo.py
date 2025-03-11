import os
import json
import logging
from pymongo import MongoClient

def load_and_delete_function():
    
    json_file_dir = "/opt/airflow/data/json_files"
    mongo_host = "mongodb"
    mongo_port = 27017
    database_name = "youtube_data"

    client = MongoClient(f"mongodb://root:example@{mongo_host}:{mongo_port}/")
    db = client[database_name]

    logging.info(f"Connected to MongoDB at {mongo_host}:{mongo_port}")

    for filename in os.listdir(json_file_dir):
        if filename.endswith(".json"):
            topic_name = filename.replace(".json", "")
            collection = db[topic_name]
            
            json_file_path = os.path.join(json_file_dir, filename)

            with open(json_file_path, 'r') as file:
                data = json.load(file)
                
            if data.get("items"):
                logging.info(f"Inserting {len(data['items'])} records into '{topic_name}' collection")
                
                # Insert each video dictionary as a separate document
                collection.insert_many(data["items"])

                logging.info(f"Successfully inserted {len(data['items'])} records into '{topic_name}' collection")

                # Deletion of the JSON file after insertion
                os.remove(json_file_path)
                logging.info(f"Deleted {filename} file")

            else:
                logging.info(f"No data found in {filename} file")
        
        else:
            logging.info(f"There are no available JSON files in {json_file_dir}")

    logging.info("Finished inserting JSON data into MongoDB")