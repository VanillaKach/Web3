import json
import logging
import pandas as pd
from datetime import datetime
from src.utils import get_exchange_rate, fetch_event_data
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Настройка логгирования
logging.basicConfig(level=logging.INFO) # Страница «Главная» --------------------------------------------

def main_page(date_time_str):
    try:
        # Преобразование строки даты и времени в объект datetime
        date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

        # Получаем курс валют с помощью вспомогательной функции
        exchange_rate = get_exchange_rate()

        # Формируем ответ в формате JSON
        response = {
            "date_time": date_time.strftime('%Y-%m-%d %H:%M:%S'),
            "exchange_rate": exchange_rate
        }

        # Логируем информацию о выполнении
        logging.info("Главная страница успешно обработана.")
        return json.dumps(response, ensure_ascii=False, indent=4)

    except Exception as e:
        logging.error(f"Ошибка при обработке главной страницы: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=4)


logging.basicConfig(level=logging.INFO) # Страница «События» --------------------------------------------

def events_page(df: pd.DataFrame):
    try:
        # Проверяем, есть ли данные в DataFrame
        if df.empty:
            logging.warning("Получен пустой DataFrame.")
            return json.dumps({"error": "Нет данных для отображения."}, ensure_ascii=False, indent=4)

        # Преобразуем DataFrame в список словарей
        events = df.to_dict(orient='records')

        # Логируем информацию о выполнении
        logging.info("Страница событий успешно обработана.")
        return json.dumps(events, ensure_ascii=False, indent=4)

    except Exception as e:
        logging.error(f"Ошибка при обработке страницы событий: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=4)
