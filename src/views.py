import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple

from src.utils import get_exchange_rate, get_stock_prices, get_transaction_data

# Настройка логгирования
logging.basicConfig(level=logging.INFO)

# ----------------------- Код для задач "Главная" -----------------------


def get_greeting() -> str:
    """
    Возвращает приветствие в зависимости от времени суток.

    :return: Приветствие
    """
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def main_page(date_time_str: str) -> str:
    """
    Обрабатывает главную страницу и возвращает данные в формате JSON.

    :param date_time_str: Строка с датой и временем в формате 'YYYY-MM-DD HH:MM:SS'
    :return: JSON-строка с данными или сообщение об ошибке
    """
    try:
        # Преобразование строки даты и времени в объект datetime
        date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

        # Получаем информацию о транзакциях
        transactions_summary = get_transaction_data(date_time, date_time)

        # Формируем JSON-ответ
        response: Dict[str, Any] = {
            "greeting": get_greeting(),
            "cards": transactions_summary["cards"],
            "top_transactions": transactions_summary["top_transactions"],
            "currency_rates": get_exchange_rate(),
            "stock_prices": get_stock_prices(),
        }

        # Логируем информацию о выполнении
        logging.info("Главная страница успешно обработана.")
        return json.dumps(response, ensure_ascii=False, indent=4)

    except Exception as e:
        logging.error(f"Ошибка при обработке главной страницы: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=4)


# ----------------------- Код для задач "События" -----------------------


def get_date_range(date: datetime, period: str) -> Tuple[datetime, datetime]:
    """
    Определяет диапазон дат в зависимости от указанного периода.

    :param date: Дата, для которой определяется диапазон
    :param period: Период (W, M, Y, ALL)
    :return: Начальная и конечная дата диапазона
    """
    if period == "W":
        start_date = date - timedelta(days=date.weekday())
        end_date = date
    elif period == "M":
        start_date = date.replace(day=1)
        end_date = date
    elif period == "Y":
        start_date = date.replace(month=1, day=1)
        end_date = date
    elif period == "ALL":
        start_date = datetime.min
        end_date = date
    else:
        raise ValueError("Неверный период. Используйте W, M, Y или ALL.")

    return start_date, end_date


def events_page(date_str: str, period: Optional[str] = "M") -> str:
    """
    Обрабатывает данные о событиях и возвращает данные в формате JSON.

    :param date_str: Дата в формате YYYY-MM-DD
    :param period: Необязательный параметр для диапазона данных
    :return: JSON-строка с данными о расходах и поступлениях
    """
    try:
        # Преобразование строки даты в объект datetime
        date = datetime.strptime(date_str, "%Y-%m-%d")
        # Проверяем, что period не None
        if period is None:
            period = "M"  # Устанавливаем значение по умолчанию
        # Получаем диапазон дат
        start_date, end_date = get_date_range(date, period)

        # Получаем данные о транзакциях
        transaction_data = get_transaction_data(start_date, end_date)

        # Формируем JSON-ответ
        response = {
            "expenses": {
                "total_amount": round(transaction_data["expenses"]["total"]),
                "main": transaction_data["expenses"]["categories"],
                "transfers_and_cash": transaction_data["expenses"]["transfers_and_cash"],
            },
            "income": {
                "total_amount": round(transaction_data["income"]["total"]),
                "main": transaction_data["income"]["categories"],
            },
            "currency_rates": get_exchange_rate(),
            "stock_prices": get_stock_prices(),
        }

        # Логируем информацию о выполнении
        logging.info("Страница событий успешно обработана.")
        return json.dumps(response, ensure_ascii=False, indent=4)

    except Exception as e:
        logging.error(f"Ошибка при обработке страницы событий: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=4)
