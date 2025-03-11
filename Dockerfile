FROM apache/airflow:2.10.5

# Install pymongo inside Airflow image
RUN pip install pymongo