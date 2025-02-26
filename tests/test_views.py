import json
from datetime import datetime
from typing import Any, Dict
from unittest import mock

import pytest

from src.views import events_page, get_date_range, get_greeting, main_page


# Тест для get_greeting
def test_get_greeting() -> None:
    with mock.patch("src.views.datetime") as mock_datetime:
        mock_datetime.now.return_value.hour = 10
        assert get_greeting() == "Доброе утро"

        mock_datetime.now.return_value.hour = 14
        assert get_greeting() == "Добрый день"

        mock_datetime.now.return_value.hour = 19
        assert get_greeting() == "Добрый вечер"

        mock_datetime.now.return_value.hour = 1
        assert get_greeting() == "Доброй ночи"


# Тест для main_page
@mock.patch("src.views.get_transaction_data")
@mock.patch("src.views.get_exchange_rate")
@mock.patch("src.views.get_stock_prices")
def test_main_page(
    mock_get_stock_prices: mock.Mock, mock_get_exchange_rate: mock.Mock, mock_get_transaction_data: mock.Mock
) -> None:
    mock_get_transaction_data.return_value = {"cards": [], "top_transactions": []}
    mock_get_exchange_rate.return_value = [{"currency": "USD", "rate": 74.23}]
    mock_get_stock_prices.return_value = [{"stock": "AAPL", "price": 150.12}]

    response: str = main_page("2021-12-31 12:00:00")
    response_data: Dict[str, Any] = json.loads(response)

    assert response_data["greeting"] is not None
    assert response_data["cards"] == []
    assert response_data["top_transactions"] == []
    assert response_data["currency_rates"] == [{"currency": "USD", "rate": 74.23}]
    assert response_data["stock_prices"] == [{"stock": "AAPL", "price": 150.12}]


@mock.patch("src.views.get_transaction_data")
def test_main_page_invalid_date(mock_get_transaction_data: mock.Mock) -> None:
    mock_get_transaction_data.side_effect = Exception("Invalid date format")

    response: str = main_page("invalid-date")
    response_data: Dict[str, Any] = json.loads(response)

    assert "error" in response_data
    assert response_data["error"] == "Invalid date format"


# Тест для get_date_range
def test_get_date_range() -> None:
    date: datetime = datetime(2021, 12, 15)

    start: datetime
    end: datetime

    start, end = get_date_range(date, "W")
    assert start <= date <= end

    start, end = get_date_range(date, "M")
    assert start.day == 1
    assert end == date

    start, end = get_date_range(date, "Y")
    assert start.month == 1
    assert start.day == 1
    assert end == date

    start, end = get_date_range(date, "ALL")
    assert start == datetime.min
    assert end == date

    with pytest.raises(ValueError, match="Неверный период. Используйте W, M, Y или ALL."):
        get_date_range(date, "INVALID")


# Тест для events_page
@mock.patch("src.views.get_transaction_data")
@mock.patch("src.views.get_exchange_rate")
@mock.patch("src.views.get_stock_prices")
def test_events_page(
    mock_get_stock_prices: mock.Mock, mock_get_exchange_rate: mock.Mock, mock_get_transaction_data: mock.Mock
) -> None:
    mock_get_transaction_data.return_value = {
        "expenses": {"total": -100, "categories": [], "transfers_and_cash": []},
        "income": {"total": 200, "categories": []},
    }
    mock_get_exchange_rate.return_value = [{"currency": "USD", "rate": 74.23}]
    mock_get_stock_prices.return_value = [{"stock": "AAPL", "price": 150.12}]

    response: str = events_page("2021-12-31")
    response_data: Dict[str, Any] = json.loads(response)

    assert response_data["expenses"]["total_amount"] == -100
    assert response_data["income"]["total_amount"] == 200
    assert response_data["currency_rates"] == [{"currency": "USD", "rate": 74.23}]
    assert response_data["stock_prices"] == [{"stock": "AAPL", "price": 150.12}]


@mock.patch("src.views.get_transaction_data")
def test_events_page_invalid_date(mock_get_transaction_data: mock.Mock) -> None:
    mock_get_transaction_data.side_effect = Exception("Invalid date format")

    response: str = events_page("invalid-date")
    response_data: Dict[str, Any] = json.loads(response)

    assert "error" in response_data
    assert response_data["error"] == "Invalid date format"


if __name__ == "__main__":
    pytest.main()
