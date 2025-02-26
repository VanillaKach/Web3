import json
import logging
from datetime import datetime, timedelta
from typing import Any, Callable, Optional, Dict, Tuple

import pandas as pd

# Настройка логгирования
logging.basicConfig(level=logging.INFO)


# Декоратор для записи отчета в файл
def save_report_to_file(file_name: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., str]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., str]:
        def wrapper(*args: Tuple, **kwargs: Dict) -> str:
            result = func(*args, **kwargs)
            result_json = json.dumps(result, ensure_ascii=False, indent=4)

            # Используем имя файла по умолчанию, если не передано
            save_file_name = file_name if file_name is not None else "report.json"

            with open(save_file_name, "w", encoding="utf-8") as f:
                f.write(result_json)
            logging.info(f"Отчет сохранен в файл: {save_file_name}")
            return result_json

        return wrapper

    return decorator


# ----------------------- Отчет «Траты по категории» -----------------------


@save_report_to_file()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает траты по заданной категории за последние три месяца.

    :param transactions: DataFrame с транзакциями
    :param category: Название категории
    :param date: Опциональная дата
    :return: DataFrame с тратами по категории
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    end_date = datetime.strptime(date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=90)

    filtered_transactions = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= end_date)
    ]

    total_spending = filtered_transactions["Сумма операции"].sum()
    logging.info(f"Траты по категории '{category}': {total_spending}")

    return pd.DataFrame({"category": [category], "total_spending": [total_spending]})


# ----------------------- Отчет «Траты по дням недели» -----------------------


@save_report_to_file()
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает средние траты в каждый из дней недели за последние три месяца.

    :param transactions: DataFrame с транзакциями
    :param date: Опциональная дата
    :return: DataFrame со средними тратами по дням недели
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    end_date = datetime.strptime(date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=90)

    filtered_transactions = transactions[
        (transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= end_date)
    ]

    filtered_transactions["День недели"] = filtered_transactions["Дата операции"].dt.day_name()
    average_spending = filtered_transactions.groupby("День недели")["Сумма операции"].mean().reset_index()

    logging.info(f"Средние траты по дням недели: {average_spending}")

    return average_spending


# ----------------------- Отчет «Траты в рабочий/выходной день» -----------------------


@save_report_to_file()
def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает средние траты в рабочий и в выходной день за последние три месяца.

    :param transactions: DataFrame с транзакциями
    :param date: Опциональная дата
    :return: DataFrame со средними тратами в рабочий и выходной день
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    end_date = datetime.strptime(date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=90)

    filtered_transactions = transactions[
        (transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= end_date)
    ]

    filtered_transactions["День недели"] = filtered_transactions["Дата операции"].dt.dayofweek
    average_spending = (
        filtered_transactions.groupby(filtered_transactions["День недели"] < 5)["Сумма операции"].mean().reset_index()
    )

    # Правильное присвоение значений
    average_spending.columns = pd.Index(["Рабочий день", "Средние траты"])

    logging.info(f"Средние траты в рабочий и выходной день: {average_spending}")

    return average_spending
