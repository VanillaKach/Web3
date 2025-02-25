import json
import logging
import re
from datetime import datetime
from typing import Any, Dict, List

# Настройка логгирования
logging.basicConfig(level=logging.INFO)


# ----------------------- Сервис «Выгодные категории повышенного кешбэка» -----------------------


def profitable_categories(data: List[Dict[str, Any]], year: int, month: int) -> str:
    """
    Анализирует выгодные категории повышенного кешбэка.

    :param data: Список транзакций
    :param year: Год для анализа
    :param month: Месяц для анализа
    :return: JSON с анализом кешбэка по категориям
    """
    cashback_by_category = {}

    for transaction in data:
        transaction_date = datetime.strptime(transaction["Дата операции"], "%Y-%m-%d")
        if transaction_date.year == year and transaction_date.month == month:
            category = transaction["Категория"]
            amount = transaction["Сумма операции"]

            if category not in cashback_by_category:
                cashback_by_category[category] = 0
            cashback_by_category[category] += amount * 0.1  # Предположим кешбэк 10%

    logging.info("Анализ выгодных категорий завершен.")
    return json.dumps(cashback_by_category, ensure_ascii=False)


# ----------------------- Сервис «Инвесткопилка» -----------------------


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Рассчитывает сумму, отложенную в «Инвесткопилку».

    :param month: Месяц для расчета (в формате 'YYYY-MM')
    :param transactions: Список транзакций
    :param limit: Порог округления
    :return: Сумма, отложенная в «Инвесткопилку»
    """
    total_saved = 0.0
    month_year = datetime.strptime(month, "%Y-%m")

    for transaction in transactions:
        transaction_date = datetime.strptime(transaction["Дата операции"], "%Y-%m-%d")
        if transaction_date.month == month_year.month and transaction_date.year == month_year.year:
            original_amount = transaction["Сумма операции"]
            rounded_amount = (original_amount // limit + 1) * limit
            total_saved += rounded_amount - original_amount

    logging.info("Расчет инвесткопилки завершен. Сумма отложенной суммы: %.2f", total_saved)
    return total_saved


# ----------------------- Сервис «Простой поиск» -----------------------


def simple_search(query: str, transactions: List[Dict[str, Any]]) -> str:
    """
    Выполняет простой поиск по транзакциям.

    :param query: Строка для поиска
    :param transactions: Список транзакций
    :return: JSON со всеми соответствующими транзакциями
    """
    results = [
        transaction
        for transaction in transactions
        if query.lower() in transaction["Описание"].lower() or query.lower() in transaction["Категория"].lower()
    ]

    logging.info("Простой поиск завершен. Найдено %d транзакций.", len(results))
    return json.dumps(results, ensure_ascii=False)


# ----------------------- Сервис «Поиск по телефонным номерам» -----------------------


def search_by_phone(transactions: List[Dict[str, Any]]) -> str:
    """
    Выполняет поиск транзакций по телефонным номерам.

    :param transactions: Список транзакций
    :return: JSON со всеми транзакциями, содержащими телефонные номера
    """
    phone_pattern = re.compile(r"\+?\d[\d -]{7,}\d")
    results = [transaction for transaction in transactions if phone_pattern.search(transaction["Описание"])]

    logging.info("Поиск по телефонным номерам завершен. Найдено %d транзакций.", len(results))
    return json.dumps(results, ensure_ascii=False)


# ----------------------- Сервис «Поиск переводов физическим лицам» -----------------------


def search_transfers_to_individuals(transactions: List[Dict[str, Any]]) -> str:
    """
    Выполняет поиск переводов физическим лицам.

    :param transactions: Список транзакций
    :return: JSON со всеми транзакциями, относящимися к переводам физлицам
    """
    results = [
        transaction
        for transaction in transactions
        if transaction["Категория"] == "Переводы" and re.search(r"\w+ \w\.", transaction["Описание"])
    ]

    logging.info("Поиск переводов физическим лицам завершен. Найдено %d транзакций.", len(results))
    return json.dumps(results, ensure_ascii=False)
