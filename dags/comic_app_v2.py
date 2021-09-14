import os
import json
import time
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.slack_operator import SlackAPIPostOperator

default_args = {
    'owner': 'Meng Lee',
    'start_date': datetime(2100, 1, 1, 0, 0),
    'schedule_interval': '@daily',
    'retries': 2,
    'retry_delay': timedelta(minutes=1)
}


def process_metadata(mode, **context):
    if mode == 'read':
        print("取得使用者的閱讀紀錄")
    elif mode == 'write':
        print("更新閱讀紀錄")


def check_comic_info(**context):
    all_comic_info = context['task_instance'].xcom_pull(task_ids='get_read_history')
    print("去漫畫網站看有沒有新的章節")

    # anything_new = time.time() % 2 > 1
    anything_new = True
    return anything_new, all_comic_info


def decide_what_to_do(**context):
    anything_new, all_comic_info = context['task_instance'].xcom_pull(task_ids='check_comic_info')

    print("跟紀錄比較，有沒有新連載？")
    if anything_new:
        return 'yes_generate_notification'
    else:
        return 'no_do_nothing'

def get_token():
    file_dir = os.path.dirname(__file__)
    token_path = os.path.join(file_dir, '../data/credentials/slack.json')
    with open(token_path, 'r') as fp:
        token = json.load(fp)['token']
        return token

def generate_message(**context):
    _, all_comic_info = context['task_instance'].xcom_pull(task_ids='check_comic_info')
    print("產生要寄給 Slack 的訊息內容並存成檔案")


with DAG('comic_app_v2', default_args=default_args) as dag:

    get_read_history = PythonOperator(
        task_id='get_read_history',
        python_callable=process_metadata,
        op_args=['read']
    )

    check_comic_info = PythonOperator(
        task_id='check_comic_info',
        python_callable=check_comic_info,
    )

    decide_what_to_do = BranchPythonOperator(
        task_id='new_comic_available',
        python_callable=decide_what_to_do,
    )

    update_read_history = PythonOperator(
        task_id='update_read_history',
        python_callable=process_metadata,
        op_args=['write'],
    )

    generate_notification = PythonOperator(
        task_id='yes_generate_notification',
        python_callable=generate_message,
    )

    send_notification = SlackAPIPostOperator(
        task_id='send_notification',
        token=get_token(),
        channel='#comic-notification',
        text="[{{ ds }}] 海賊王有新番了!",
        icon_url='http://airbnb.io/img/projects/airflow3.png'
    )

    do_nothing = DummyOperator(task_id='no_do_nothing')

    # define workflow
    get_read_history >> check_comic_info >> decide_what_to_do
    decide_what_to_do >> generate_notification
    decide_what_to_do >> do_nothing
    generate_notification >> send_notification >> update_read_history
