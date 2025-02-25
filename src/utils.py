import requests
import os
import pandas as pd
from dotenv import load_dotenv

# Загрузка переменных окружения ------------------- Для страницы «Главная» ----------------------
load_dotenv()

def get_exchange_rate():
    api_key = os.getenv('EXCHANGE_API_KEY')
    url = f'https://api.exchangeratesapi.io/latest?access_key={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['rates']  # Возвращаем курсы валют
    else:
        raise Exception("Не удалось получить данные от API.")


# Загрузка переменных окружения ------------------- Для страницы «События» -----------------------
load_dotenv()

def fetch_event_data(api_endpoint: str) -> pd.DataFrame:
    api_key = os.getenv('EXCHANGE_API_KEY')
    response = requests.get(f"{api_endpoint}?access_key={api_key}")

    if response.status_code == 200:
        data = response.json()
        # Преобразуем полученные данные в DataFrame
        return pd.DataFrame(data['events'])  # Здесь предполагается, что API возвращает события в нужном формате
    else:
        raise Exception("Не удалось получить данные от API.")
