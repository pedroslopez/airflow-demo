
import requests
import csv
from airflow import DAG
from datetime import datetime

from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresHook
from airflow.providers.discord.operators.discord_webhook import DiscordWebhookOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

csv_path = "/Users/pedro/grouparoo/airflow-test/data.csv"
webhook_endpoint = "webhooks/SOME_SECRET/WEBHOOK"

def download_csv():
    resp = requests.get("https://raw.githubusercontent.com/grouparoo/grouparoo/main/core/__tests__/data/records-10.csv")
    with open(csv_path, "wb") as f:
        for chunk in resp:
            f.write(chunk)

def load_csv():
    pg = PostgresHook(postgres_conn_id="grouparoo_profile_db")

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        rows = [tuple(row) for row in reader][1:]
        pg.insert_rows(
            "profiles", 
            rows, 
            target_fields=[
                "id", 
                "first_name", 
                "last_name", 
                "email", 
                "gender", 
                "ip_address", 
                "ios_app", 
                "android_app", 
                "vip", 
                "ltv"
            ], 
            replace=True,
            replace_index="id"
        )

with DAG(
    'grouparoo_demo', 
    start_date=days_ago(1),
    schedule_interval=None
) as dag:
    download = PythonOperator(
        task_id="download_csv", 
        python_callable=download_csv
    )

    load = PythonOperator(
        task_id="load_data", 
        python_callable=load_csv
    )

    grouparoo = BashOperator(
        task_id="run_grouparoo", 
        bash_command="cd ~/grouparoo/airflow-test && grouparoo run"
    )

    notify_end = DiscordWebhookOperator(
        task_id="notify_end", 
        http_conn_id="discord", 
        webhook_endpoint=webhook_endpoint, 
        message="Your workflow has finished running!"
    )

    download >> load >> grouparoo >> notify_end

