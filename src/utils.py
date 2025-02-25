import os
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
import requests
from dotenv import load_dotenv  # type: ignore

# Загрузка переменных окружения
load_dotenv()


# ----------------------- Функции для получения данных -----------------------

def get_exchange_rate() -> List[Dict[str, float]]:
    """
    Получает курс валют из API.

    :return: Список курсов валют
    :raises Exception: Если не удалось получить данные от API
    """
    api_key = os.getenv('EXCHANGE_API_KEY')
    url = f'https://api.exchangeratesapi.io/latest?access_key={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return [{"currency": currency, "rate": rate} for currency, rate in data['rates'].items()]
    else:
        raise Exception("Не удалось получить данные от API.")


def get_stock_prices() -> List[Dict[str, Any]]:
    """
    Получает цены акций из S&P 500.

    :return: Список цен акций
    """
    return [
        {"stock": "AAPL", "price": 150.12},
        {"stock": "AMZN", "price": 3173.18},
        {"stock": "GOOGL", "price": 2742.39},
        {"stock": "MSFT", "price": 296.71},
        {"stock": "TSLA", "price": 1007.08},
    ]


def get_transaction_data(start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """
    Получает данные о транзакциях в заданном диапазоне дат.

    :param start_date: Начальная дата диапазона
    :param end_date: Конечная дата диапазона
    :return: Словарь с данными о расходах и поступлениях
    """
    df = pd.read_excel('data/operations.xlsx')  # Укажите путь к вашему файлу
    df['Дата операции'] = pd.to_datetime(df['Дата операции'])

    # Фильтрация по диапазону дат
    filtered_df = df[(df['Дата операции'] >= start_date) & (df['Дата операции'] <= end_date)]

    # Расходы
    expenses_total = filtered_df['Сумма платежа'].sum()
    expenses_by_category = filtered_df.groupby('Категория')['Сумма платежа'].sum().nlargest(7).reset_index()

    other_expenses = filtered_df.groupby('Категория')['Сумма платежа'].sum().sum() - expenses_by_category[
        'Сумма платежа'].sum()
    if other_expenses > 0:
        expenses_by_category = expenses_by_category.append({'Категория': 'Остальное', 'Сумма платежа': other_expenses},
                                                           ignore_index=True)

    # Переводы и наличные
    transfers_and_cash = filtered_df[filtered_df['Категория'].isin(['Наличные', 'Переводы'])]
    transfers_and_cash_summary = transfers_and_cash.groupby('Категория')['Сумма платежа'].sum().reset_index()

    # Поступления
    income_total = filtered_df[filtered_df['Статус'] == 'Поступление']['Сумма платежа'].sum()
    income_by_category = filtered_df[filtered_df['Статус'] == 'Поступление'].groupby('Категория')[
        'Сумма платежа'].sum().nlargest(5).reset_index()

    return {
        "expenses": {
            "total": expenses_total,
            "categories": expenses_by_category.to_dict(orient='records'),
            "transfers_and_cash": transfers_and_cash_summary.to_dict(orient='records')
        },
        "income": {
            "total": income_total,
            "categories": income_by_category.to_dict(orient='records')
        }
    }
