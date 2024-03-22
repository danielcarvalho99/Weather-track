from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()

KELVIN = 273.15
API_KEY = os.getenv("API_KEY")

def get_json():
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Aracaju,br&APPID={API_KEY}"
    r = requests.get(url)
    return r.json()

def get_main_info(ti):
    infos = {}
    
    json= ti.xcom_pull(task_ids='get_json')

    infos['Cidade'] = json['name']
    infos['Temperatura'] = f"{round(json['main']['temp'] - KELVIN, 2)} ºC"
    infos['Sensação'] = f"{round(json['main']['feels_like'] - KELVIN, 2)} ºC"
    infos['Umidade'] = f"{json['main']['humidity']} %"
    
    return infos

def generate_text(ti):
    info = ti.xcom_pull(task_ids='get_main_info')
    text = f"\nInformações de {info['Cidade']} no momento:\n"
    
    for key,val in info.items():
        if key == 'Cidade':
            continue
        
        text += ''.join(f"A {key} no momento é de {val}\n")
    
    return text

def print_info(ti):
    info = ti.xcom_pull(task_ids='generate_text')
    print(info)

with DAG(
        dag_id="Weather_DAG",
        start_date=datetime(2024,3,22),
        schedule = "@hourly",
        catchup=False,
):

    get_json = PythonOperator(
        task_id = 'get_json',
        python_callable = get_json)
    
    get_main_info = PythonOperator(
        task_id = 'get_main_info',
        python_callable = get_main_info)

    generate_text = PythonOperator(
        task_id = 'generate_text',
        python_callable = generate_text)
    
    print_info = PythonOperator(
        task_id='print_info',
        python_callable=print_info
    )
    

(get_json >> get_main_info >> generate_text >> print_info)

