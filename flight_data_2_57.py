from airflow import DAG
from airflow.decorators import task
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
from datetime import datetime, timedelta
import pandas as pd
import os
import time

local_file_path = "/home/growlt257/Desktop/Flight_Data/modified_flight_data.csv"
batch_size = 160000  # Define your batch size here

with DAG(
    "data_of_flight_2_57",
    start_date=datetime(2023, 7, 5),
    doc_md=__doc__,
    max_active_runs=1,
    schedule_interval="@daily",  # Runs once every 24 hours
    default_args={
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
    },
    catchup=False,  # Enable if you don't want historical dag runs to run
) as dag:


    t0 = DummyOperator(task_id="start")

    @task(task_id="split_csv_into_batches")
    def split_csv_into_batches():
        # Read the CSV file
        df = pd.read_csv(local_file_path)
        total_rows = len(df)
        batches = [df[i:i + batch_size] for i in range(0, total_rows, batch_size)]
        
        # Save batches as CSV files
        batch_file_paths = []
        for i, batch_df in enumerate(batches):
            batch_file_path = f"/tmp/batch_{i + 1}_of_{len(batches)}.csv"
            batch_df.to_csv(batch_file_path, index=False)
            batch_file_paths.append(batch_file_path)
        
        return batch_file_paths  # Return the list of batch file paths

    @task(task_id="convert_csv_to_parquet")
    def convert_csv_to_parquet(batch_file_paths: list):
        parquet_file_paths = []
        for batch_file_path in batch_file_paths:
            # Read the batch CSV file
            batch_df = pd.read_csv(batch_file_path)
            
            # Convert to Parquet
            parquet_file_path = batch_file_path.replace('.csv', '.parquet')
            batch_df.to_parquet(parquet_file_path, index=False)
            parquet_file_paths.append(parquet_file_path)
            
            # Remove the original CSV file to save space
            os.remove(batch_file_path)
        
        return parquet_file_paths

    def upload_batch_to_azure_blob(parquet_file_path: str):
        # Instantiate Azure Blob hook
        azurehook = WasbHook(wasb_conn_id="flight-data-storage-account-connection")

        # Generate a blob name based on the Parquet file path (ensuring uniqueness)
        blob_name = os.path.basename(parquet_file_path)  # Remove directory path

        # Upload the batch to Azure Blob Storage (overwriting any existing blobs with the same name)
        azurehook.load_file(file_path=parquet_file_path, container_name="flightdatabatches", blob_name=blob_name, overwrite=True)

    @task(task_id="upload_batches_to_azure")
    def upload_batches_to_azure(parquet_file_paths: list):
        for parquet_file_path in parquet_file_paths:
            upload_batch_to_azure_blob(parquet_file_path)
            time.sleep(300)  # Sleep for 180 seconds (3 minutes) after each upload

    split_batches_task = split_csv_into_batches()
    convert_to_parquet_task = convert_csv_to_parquet(split_batches_task)
    upload_batches_task = upload_batches_to_azure(convert_to_parquet_task)

    t0 >> split_batches_task >> convert_to_parquet_task >> upload_batches_task
