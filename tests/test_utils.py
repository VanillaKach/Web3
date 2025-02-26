from datetime import datetime
from typing import Any, Dict, List
from unittest import mock

import pandas as pd
import pytest

from src.utils import get_exchange_rate, get_stock_prices, get_transaction_data


# Фикстура для генерации тестовых данных
@pytest.fixture
def mock_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(["31.12.2021 16:44:00", "31.12.2021 16:42:04"]),
            "Сумма платежа": [-160.89, -64.00],
            "Категория": ["Супермаркеты", "Супермаркеты"],
            "Статус": ["OK", "OK"],
        }
    )


# Тест для get_exchange_rate
@mock.patch("src.utils.requests.get")
def test_get_exchange_rate(mock_get: mock.Mock) -> None:
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"rates": {"USD": 74.23, "EUR": 88.12}}

    rates: List[Dict[str, float]] = get_exchange_rate()
    assert len(rates) == 2
    assert rates[0]["currency"] == "USD"
    assert rates[0]["rate"] == 74.23


@mock.patch("src.utils.requests.get")
def test_get_exchange_rate_failure(mock_get: mock.Mock) -> None:
    mock_get.return_value.status_code = 400
    with pytest.raises(Exception, match="Не удалось получить данные от API."):
        get_exchange_rate()


# Тест для get_stock_prices
def test_get_stock_prices() -> None:
    prices: List[Dict[str, Any]] = get_stock_prices()
    assert len(prices) == 5
    assert prices[0]["stock"] == "AAPL"
    assert prices[0]["price"] == 150.12


# Тест для get_transaction_data
@mock.patch("src.utils.pd.read_excel")
def test_get_transaction_data(mock_read_excel: mock.Mock, mock_data: pd.DataFrame) -> None:
    mock_read_excel.return_value = mock_data

    start_date: datetime = datetime(2021, 12, 31)
    end_date: datetime = datetime(2021, 12, 31)

    result: Dict[str, Any] = get_transaction_data(start_date, end_date)

    assert result["expenses"]["total"] == -224.89
    assert len(result["expenses"]["categories"]) == 1
    assert result["income"]["total"] == 0
    assert len(result["income"]["categories"]) == 0


if __name__ == "__main__":
    pytest.main()
