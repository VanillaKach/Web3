import json
from typing import Any, Dict, List

from src.services import investment_bank, profitable_categories, search_by_phone, search_transfers_to_individuals, simple_search


# Тест для profitable_categories
def test_profitable_categories() -> None:
    data: List[Dict[str, Any]] = [
        {"Дата операции": "2023-01-15", "Категория": "Еда", "Сумма операции": 100},
        {"Дата операции": "2023-01-20", "Категория": "Транспорт", "Сумма операции": 50},
        {"Дата операции": "2023-02-10", "Категория": "Еда", "Сумма операции": 200},
    ]
    result: str = profitable_categories(data, 2023, 1)
    expected_result: Dict[str, float] = {"Еда": 10.0, "Транспорт": 5.0}
    assert json.loads(result) == expected_result


# Тест для investment_bank
def test_investment_bank() -> None:
    transactions: List[Dict[str, Any]] = [
        {"Дата операции": "2023-01-15", "Сумма операции": 100},
        {"Дата операции": "2023-01-20", "Сумма операции": 75},
        {"Дата операции": "2023-02-10", "Сумма операции": 50},
    ]
    result: float = investment_bank("2023-01", transactions, 10)
    assert result == 25.0  # 10 - 100% округление до 110


# Тест для simple_search
def test_simple_search() -> None:
    transactions: List[Dict[str, Any]] = [
        {"Описание": "Покупка еды", "Категория": "Еда"},
        {"Описание": "Поездка на такси", "Категория": "Транспорт"},
        {"Описание": "Покупка одежды", "Категория": "Одежда"},
    ]
    result: str = simple_search("еда", transactions)
    expected_result: List[Dict[str, Any]] = [{"Описание": "Покупка еды", "Категория": "Еда"}]
    assert json.loads(result) == expected_result


# Тест для search_by_phone
def test_search_by_phone() -> None:
    transactions: List[Dict[str, Any]] = [
        {"Описание": "Оплата по номеру +123456789", "Категория": "Переводы"},
        {"Описание": "Оплата по номеру 987654321", "Категория": "Переводы"},
        {"Описание": "Без номера", "Категория": "Другие"},
    ]
    result: str = search_by_phone(transactions)
    expected_result: List[Dict[str, Any]] = [
        {"Описание": "Оплата по номеру +123456789", "Категория": "Переводы"},
        {"Описание": "Оплата по номеру 987654321", "Категория": "Переводы"},
    ]
    assert json.loads(result) == expected_result


# Тест для search_transfers_to_individuals
def test_search_transfers_to_individuals() -> None:
    transactions: List[Dict[str, Any]] = [
        {"Описание": "Перевод Иванов И.И.", "Категория": "Переводы"},
        {"Описание": "Перевод на карту", "Категория": "Переводы"},
        {"Описание": "Перевод Петров П.П.", "Категория": "Переводы"},
    ]
    result: str = search_transfers_to_individuals(transactions)
    expected_result: List
