import pytest
from src.transactions import process_bank_search, process_bank_operations


@pytest.fixture
def sample_data():
    return [
        {"description": "Перевод организации", "status": "EXECUTED"},
        {"description": "Открытие вклада", "status": "EXECUTED"},
        {"description": "Покупка товаров", "status": "CANCELED"},
    ]


def test_search_operations(sample_data):
    """Тестирует поиск операций."""
    result = process_bank_search(sample_data, "перевод")
    assert len(result) == 1
    assert result[0]["description"] == "Перевод организации"


def test_count_operations(sample_data):
    """Тестирует подсчет операций."""
    categories = ["Перевод организации", "Открытие вклада", "Платеж"]
    result = process_bank_operations(sample_data, categories)
    assert result["Перевод организации"] == 1
    assert result["Открытие вклада"] == 1
    assert result["Платеж"] == 0


def test_empty_data_handling():
    """Тестирует обработку пустых данных."""
    result = process_bank_operations([], ["Категория"])
    assert result == {"Категория": 0}


def test_none_description_handling():
    """Тестирует обработку None в описании."""
    result = process_bank_operations([{"description": None}], ["Категория"])
    assert result == {"Категория": 0}


def test_empty_description_handling():
    """Тестирует обработку пустого описания."""
    result = process_bank_operations([{"description": ""}], ["Категория"])
    assert result == {"Категория": 0}


def test_missing_description_handling():
    """Тестирует обработку отсутствующего описания."""
    result = process_bank_operations([{}], ["Категория"])
    assert result == {"Категория": 0}
