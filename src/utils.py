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
    api_key = os.getenv("EXCHANGE_API_KEY")
    url = f"https://api.exchangeratesapi.io/latest?access_key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return [{"currency": currency, "rate": rate} for currency, rate in data["rates"].items()]
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
    df = pd.read_excel("data/operations.xlsx")
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    # Фильтрация по диапазону дат
    filtered_df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]

    # Добавляем вывод для отладки
    print("Filtered DataFrame:")
    print(filtered_df)

    # Расходы
    expenses_total = filtered_df["Сумма платежа"].sum()
    print("Total Expenses:", expenses_total)  # Вывод для отладки

    expenses_by_category = filtered_df.groupby("Категория")["Сумма платежа"].sum().nlargest(7).reset_index()
    print("Expenses by Category:")
    print(expenses_by_category)  # Вывод для отладки

    # Остальные расходы
    other_expenses = (
        filtered_df.groupby("Категория")["Сумма платежа"].sum().sum() - expenses_by_category["Сумма платежа"].sum()
    )
    if other_expenses > 0:
        new_row = pd.DataFrame({"Категория": ["Остальное"], "Сумма платежа": [other_expenses]})
        expenses_by_category = pd.concat([expenses_by_category, new_row], ignore_index=True)

    # Переводы и наличные
    transfers_and_cash = filtered_df[filtered_df["Категория"].isin(["Наличные", "Переводы"])]
    transfers_and_cash_summary = transfers_and_cash.groupby("Категория")["Сумма платежа"].sum().reset_index()

    # Поступления
    income_total = filtered_df[filtered_df["Статус"] == "Поступление"]["Сумма платежа"].sum()
    income_by_category = (
        filtered_df[filtered_df["Статус"] == "Поступление"]
        .groupby("Категория")["Сумма платежа"]
        .sum()
        .nlargest(5)
        .reset_index()
    )

    return {
        "expenses": {
            "total": expenses_total,
            "categories": expenses_by_category.to_dict(orient="records"),
            "transfers_and_cash": transfers_and_cash_summary.to_dict(orient="records"),
        },
        "income": {"total": income_total, "categories": income_by_category.to_dict(orient="records")},
    }
