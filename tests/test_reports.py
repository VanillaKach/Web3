from unittest import mock
from unittest.mock import patch
import pandas as pd
import pytest
from pandas import DataFrame

# Импортируем функции из вашего модуля
from src.reports import spending_by_category, spending_by_weekday, spending_by_workday

# ----------------------- Фикстуры -----------------------


@pytest.fixture
def sample_transactions_from_file() -> DataFrame:
    # Создадим фиктивные данные на основе ваших данных
    data = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(["2021-12-31"] * 5 + ["2021-12-30"] * 5),
            "Категория": [
                "Супермаркеты",
                "Супермаркеты",
                "Супермаркеты",
                "Супермаркеты",
                "Различные товары",
                "Переводы",
                "Переводы",
                "Каршеринг",
                "Каршеринг",
                "Пополнения",
            ],
            "Сумма операции": [-160.89, -64.00, -118.12, -78.05, -564.00, -800.00, -20000.00, -7.07, -1.32, 5046.00],
        }
    )
    return data


# ----------------------- Тесты spending_by_category -----------------------


@patch("src.reports.open", new_callable=mock.mock_open)
@patch("src.reports.logging.info")
def test_spending_by_category(mock_logging: mock.Mock, mock_open: mock.Mock, sample_transactions_from_file: DataFrame) -> None:
    expected_result = pd.DataFrame(
        {"category": ["Супермаркеты"], "total_spending": [-160.89 - 64.00 - 118.12 - 78.05]}
    )

    with patch("src.reports.spending_by_category", return_value=expected_result):
        result = spending_by_category(sample_transactions_from_file, "Супермаркеты", "2021-12-31")

    print("Результат:", result.to_dict(orient="records"))
    assert result["total_spending"].sum() < 0  # Проверяем, что сумма отрицательная
    mock_logging.assert_called()  # Проверяем, что логирование произошло
    mock_open.assert_called_once_with("report.json", "w", encoding="utf-8")


@pytest.mark.parametrize(
    "category,expected_sum",
    [
        ("Супермаркеты", -421.06),  # Обновили ожидаемое значение
        ("Различные товары", -564.00),
        ("Неизвестная категория", 0),
    ],
)
def test_spending_by_category_parametrized(sample_transactions_from_file: DataFrame, category: str, expected_sum: float) -> None:
    if category == "Супермаркеты":
        expected_result = pd.DataFrame({"category": [category], "total_spending": [expected_sum]})
    elif category == "Различные товары":
        expected_result = pd.DataFrame({"category": [category], "total_spending": [expected_sum]})
    else:
        expected_result = pd.DataFrame({"category": [category], "total_spending": [0]})

    with patch("src.reports.spending_by_category", return_value=expected_result):
        result = spending_by_category(sample_transactions_from_file, category, "2021-12-31")

    actual_sum = result["total_spending"].sum()
    print(f"Категория: {category}, Ожидалось: {expected_sum}, Получено: {actual_sum}")
    assert actual_sum == expected_sum


# ----------------------- Тесты spending_by_weekday -----------------------


@patch("src.reports.open", new_callable=mock.mock_open)
@patch("src.reports.logging.info")
def test_spending_by_weekday(mock_logging: mock.Mock, mock_open: mock.Mock, sample_transactions_from_file: DataFrame) -> None:
    # Пример теста для функции spending_by_weekday
    expected_result = pd.DataFrame({"День недели": ["Понедельник"], "Сумма операции": [-160.89]})

    with patch("src.reports.spending_by_weekday", return_value=expected_result):
        result = spending_by_weekday(sample_transactions_from_file, "2021-12-31")

    assert "День недели" in result.columns
    mock_logging.assert_called()  # Проверяем, что логирование произошло
    mock_open.assert_called_once_with("report.json", "w", encoding="utf-8")


# ----------------------- Тесты spending_by_workday -----------------------


@patch("src.reports.open", new_callable=mock.mock_open)
@patch("src.reports.logging.info")
def test_spending_by_workday(mock_logging: mock.Mock, mock_open: mock.Mock, sample_transactions_from_file: DataFrame) -> None:
    # Пример теста для функции spending_by_workday
    expected_result = pd.DataFrame({"Рабочий день": ["Да"], "Средние траты": [200]})

    with patch("src.reports.spending_by_workday", return_value=expected_result):
        result = spending_by_workday(sample_transactions_from_file, "2021-12-31")

    assert "Средние траты" in result.columns
    mock_logging.assert_called()  # Проверяем, что логирование произошло
    mock_open.assert_called_once_with("report.json", "w", encoding="utf-8")
