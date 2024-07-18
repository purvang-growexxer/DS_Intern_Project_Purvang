from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.email import send_email
from datetime import timedelta

# Define the function to send an email on failure
def notify_email(context):
    subject = f"DAG {context['task_instance_key_str']} has failed"
    html_content = f"""
    <p>DAG: {context['task_instance'].dag_id}</p>
    <p>Task: {context['task_instance'].task_id}</p>
    <p>Execution Time: {context['execution_date']}</p>
    <p>Log URL: {context['task_instance'].log_url}</p>
    """
    send_email('purvang.maheria@growexx.com', subject, html_content)

# Define the function that will intentionally fail
def fail_task():
    raise Exception("This task is designed to fail")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['purvang.maheria@growexx.com'],
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1),
    'on_failure_callback': notify_email,  # Add the failure callback here
}

with DAG(
    'intentional_failure_dag',
    default_args=default_args,
    description='A simple DAG that fails intentionally',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
) as dag:

    fail = PythonOperator(
        task_id='fail_task',
        python_callable=fail_task,
    )

    fail
