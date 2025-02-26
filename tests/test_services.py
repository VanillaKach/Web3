import json

from src.services import investment_bank, profitable_categories, search_by_phone, search_transfers_to_individuals, simple_search


def test_profitable_categories() -> None:
    """Тест для функции profitable_categories."""
    transactions = [
        {"Дата операции": "2023-01-15", "Категория": "Супермаркеты", "Сумма операции": 1000},
        {"Дата операции": "2023-01-20", "Категория": "Кафе", "Сумма операции": 500},
        {"Дата операции": "2023-01-15", "Категория": "Супермаркеты", "Сумма операции": 2000},
        {"Дата операции": "2023-02-10", "Категория": "Супермаркеты", "Сумма операции": 1500},
    ]

    expected_result = {"Супермаркеты": 300.0, "Кафе": 50.0}  # (1000 + 2000) * 0.1  # (500) * 0.1

    result = profitable_categories(transactions, 2023, 1)
    assert json.loads(result) == expected_result


def test_investment_bank() -> None:
    """Тест для функции investment_bank."""
    month = "2023-01"
    transactions = [
        {"Дата операции": "2023-01-10", "Сумма операции": 250},
        {"Дата операции": "2023-01-15", "Сумма операции": 1000},
        {"Дата операции": "2023-01-20", "Сумма операции": 500},
    ]
    limit = 100

    result = investment_bank(month, transactions, limit)
    expected_saved = (300 - 250) + (1100 - 1000) + (600 - 500)  # 50 + 100 + 100 = 250

    assert result == expected_saved


def test_simple_search() -> None:
    """Тест для функции simple_search."""
    transactions = [
        {"Описание": "Покупка в магазине", "Категория": "Супермаркеты"},
        {"Описание": "Ужин в ресторане", "Категория": "Кафе"},
        {"Описание": "Перевод другу", "Категория": "Переводы"},
    ]

    result = simple_search("магазин", transactions)
    expected = [{"Описание": "Покупка в магазине", "Категория": "Супермаркеты"}]

    assert json.loads(result) == expected

    # Проверяем поиск по категории
    result = simple_search("Кафе", transactions)
    expected = [{"Описание": "Ужин в ресторане", "Категория": "Кафе"}]

    assert json.loads(result) == expected


def test_search_by_phone() -> None:
    """Тест для функции search_by_phone."""
    transactions = [
        {"Описание": "Перевод на номер +79161234567", "Категория": "Переводы"},
        {"Описание": "Покупка в магазине", "Категория": "Супермаркеты"},
        {"Описание": "Контактный номер: +79261234567", "Категория": "Услуги"},
    ]

    result = search_by_phone(transactions)
    expected = [
        {"Описание": "Перевод на номер +79161234567", "Категория": "Переводы"},
        {"Описание": "Контактный номер: +79261234567", "Категория": "Услуги"},
    ]

    assert json.loads(result) == expected


def test_search_transfers_to_individuals() -> None:
    """Тест для функции поиска переводов физическим лицам."""
    transactions = [
        {"Описание": "Перевод другу Ивану И.", "Категория": "Переводы"},
        {"Описание": "Перевод на номер +79161234567", "Категория": "Переводы"},
        {"Описание": "Покупка в магазине", "Категория": "Супермаркеты"},
        {"Описание": "Перевод Кате", "Категория": "Переводы"},
    ]

    result = search_transfers_to_individuals(transactions)
    expected = [{"Категория": "Переводы", "Описание": "Перевод другу Ивану И."}]

    # Преобразуем результат в список словарей
    result_list = json.loads(result) if isinstance(result, str) else result

    assert result_list == expected
