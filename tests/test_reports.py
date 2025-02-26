import pandas as pd
import pytest

from typing import Any, Dict
from src.reports import spending_by_category, spending_by_weekday, spending_by_workday


# Тест для spending_by_category
def test_spending_by_category() -> None:
    transactions: pd.DataFrame = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(["2023-01-15", "2023-01-20", "2023-02-10", "2023-02-15", "2023-03-01"]),
            "Категория": ["Еда", "Транспорт", "Еда", "Еда", "Транспорт"],
            "Сумма операции": [100, 50, 200, 150, 75],
        }
    )

    result: Dict[str, Any] = spending_by_category(transactions, "Еда")
    expected_result: Dict[str, Any] = {"category": "Еда", "total_spending": 450}
    assert result == expected_result


# Тест для spending_by_weekday
def test_spending_by_weekday() -> None:
    transactions: pd.DataFrame = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(["2023-01-15", "2023-01-16", "2023-01-17", "2023-01-18", "2023-01-19"]),
            "Категория": ["Еда", "Транспорт", "Еда", "Еда", "Транспорт"],
            "Сумма операции": [100, 50, 200, 150, 75],
        }
    )

    result: pd.DataFrame = spending_by_weekday(transactions)
    expected_result: pd.DataFrame = pd.DataFrame(
        {"День недели": ["Monday", "Sunday", "Thursday"], "Сумма операции": [50.0, 100.0, 150.0]}
    )

    # Сравниваем только значения, поскольку порядок может меняться
    pd.testing.assert_frame_equal(
        result.sort_values(by="День недели").reset_index(drop=True, inplace=False),
        expected_result.sort_values(by="День недели").reset_index(drop=True, inplace=False),
    )


# Тест для spending_by_workday
def test_spending_by_workday() -> None:
    transactions: pd.DataFrame = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(
                ["2023-01-15", "2023-01-16", "2023-01-17", "2023-01-18", "2023-01-19", "2023-01-20"]
            ),
            "Категория": ["Еда", "Транспорт", "Еда", "Еда", "Транспорт", "Еда"],
            "Сумма операции": [100, 50, 200, 150, 75, 80],
        }
    )

    result: pd.DataFrame = spending_by_workday(transactions)
    expected_result: pd.DataFrame = pd.DataFrame({"Рабочий день": [False, True], "Средние траты": [100.0, 77.5]})

    # Сравниваем только значения, поскольку порядок может меняться
    pd.testing.assert_frame_equal(
        result.sort_values(by="Рабочий день").reset_index(drop=True, inplace=False),
        expected_result.sort_values(by="Рабочий день").reset_index(drop=True, inplace=False),
    )


if __name__ == "__main__":
    pytest.main()
