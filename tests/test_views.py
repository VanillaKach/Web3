from datetime import datetime
from typing import Any, Dict, Generator
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.utils import get_exchange_rate, get_stock_prices, get_transaction_data


@pytest.fixture
def mock_environment() -> Generator[None, None, None]:
    """Фикстура для мока переменных окружения."""
    with patch("os.getenv") as mock_getenv:
        mock_getenv.return_value = "mock_api_key"
        yield


@pytest.fixture
def mock_requests_get() -> Generator[MagicMock, None, None]:
    """Фикстура для мока HTTP-запросов."""
    with patch("src.utils.requests.get") as mock_get:
        yield mock_get


def test_get_exchange_rate(mock_environment: None, mock_requests_get: MagicMock) -> None:
    """Тест для проверки получения обменного курса."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "rates": {
            "USD": 1.0,
            "EUR": 0.85,
        }
    }
    mock_requests_get.return_value = mock_response

    result = get_exchange_rate()

    assert len(result) == 2
    assert result[0]["currency"] == "USD"
    assert result[0]["rate"] == 1.0
    assert result[1]["currency"] == "EUR"
    assert result[1]["rate"] == 0.85


def test_get_exchange_rate_failure(mock_environment: None, mock_requests_get: MagicMock) -> None:
    """Тест для проверки обработки ошибок при получении обменного курса."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_requests_get.return_value = mock_response

    with pytest.raises(Exception, match="Не удалось получить данные от API."):
        get_exchange_rate()


def test_get_stock_prices() -> None:
    """Тест для проверки получения цен акций."""
    result = get_stock_prices()

    assert len(result) == 5
    assert result[0]["stock"] == "AAPL"
    assert result[0]["price"] == 150.12


@pytest.fixture
def mock_read_excel() -> Generator[MagicMock, None, None]:
    """Фикстура для мока чтения из Excel."""
    with patch("src.utils.pd.read_excel") as mock_read:
        mock_df = pd.DataFrame(
            {
                "Дата операции": ["31.12.2021 16:44:00", "31.12.2021 16:42:04"],
                "Сумма платежа": [-160.89, -64.00],
                "Категория": ["Супермаркеты", "Супермаркеты"],
                "Статус": ["OK", "OK"],
            }
        )
        mock_df["Дата операции"] = pd.to_datetime(mock_df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        mock_read.return_value = mock_df
        yield mock_read


def test_get_transaction_data(mock_read_excel: None) -> None:
    """Тест для проверки получения данных о транзакциях."""
    start_date = datetime(2021, 12, 31)
    end_date = datetime(2021, 12, 31)

    result: Dict[str, Any] = get_transaction_data(start_date, end_date)

    assert result["expenses"]["total"] == 0.0
    assert len(result["expenses"]["categories"]) == 0
    assert result["income"]["total"] == 0
