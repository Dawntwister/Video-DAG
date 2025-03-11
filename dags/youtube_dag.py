from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from fetch_youtube_data import fetch_function
from load_data_to_mongo import load_and_delete_function
import textwrap

# Define default arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 2, 24),
    'retries': 1,
}

# Define DAG
with DAG(
    dag_id='is459_assignment_youtube',
    default_args=default_args,
    schedule_interval=None,  # Run manually
) as dag:

    # Define tasks
    task_1 = PythonOperator(
        task_id='youtube_data_fetch',
        python_callable=fetch_function
    )

    task_2 = PythonOperator(
        task_id='mongo_db_insert',
        python_callable=load_and_delete_function
    )

    task_1.doc_md = textwrap.dedent(
        """\
    #### Task 1 Documentation

    Fetching data from YouTube API based on topics listed in topic.txt and 
    writing the video details relating to the topic in a JSON file named after the topic
    """
    )

    task_2.doc_md = textwrap.dedent(
        """\
    #### Task 2 Documentation

    Retrieve data from created topic JSON files and loading data to MongoDB as a collection before deleting the file
    """
    )

    # Set task dependencies
    task_1 >> task_2  # Task 1 runs before Task 2