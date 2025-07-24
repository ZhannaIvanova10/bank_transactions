import pytest
from unittest.mock import patch
from src.main import (
    load_transactions,
    filter_by_status,
    filter_by_currency,
    print_transactions,
    main,
    process_bank_search,
    process_bank_operations
)


@pytest.fixture
def sample_transactions():
    return [
        {
            "description": "Перевод",
            "status": "EXECUTED",
            "date": "2023-01-01",
            "amount": 1000,
            "currency": "RUB"
        },
        {
            "description": "Покупка",
            "status": "CANCELED",
            "date": "2023-01-02",
            "amount": 50,
            "currency": "USD"
        }
    ]


def test_load_transactions_return():
    """Тестирует возвращаемый тип функции load_transactions."""
    result = load_transactions("1")
    assert isinstance(result, list)
    assert all(isinstance(tx, dict) for tx in result)


def test_load_transactions_invalid():
    """Тестирует обработку неверного типа файла."""
    with pytest.raises(ValueError):
        load_transactions("4")


def test_filter_by_status(sample_transactions):
    """Тестирует фильтрацию по статусу."""
    filtered = filter_by_status(sample_transactions, "executed")
    assert len(filtered) == 1
    assert filtered[0]["status"] == "EXECUTED"


def test_filter_by_currency(sample_transactions):
    """Тестирует фильтрацию по валюте."""
    filtered = filter_by_currency(sample_transactions, "rub")
    assert len(filtered) == 1
    assert filtered[0]["currency"] == "RUB"


def test_process_bank_search(sample_transactions):
    """Тестирует поиск транзакций по описанию."""
    result = process_bank_search(sample_transactions, "перевод")
    assert len(result) == 1
    assert result[0]["description"] == "Перевод"


def test_process_bank_operations(sample_transactions):
    """Тестирует подсчет операций по категориям."""
    result = process_bank_operations(
        sample_transactions,
        ["Перевод", "Покупка"]
    )
    assert result == {"Перевод": 1, "Покупка": 1}


@patch("builtins.input", side_effect=[
    "1", "EXECUTED", "да", "по возрастанию", "нет", "нет"
])
def test_sorting_operations(mock_input, capsys):
    """Тестирует сортировку операций."""
    main()
    captured = capsys.readouterr()
    output = captured.out
    assert "2023-01-01" in output
    assert "2023-01-02" in output


@patch("builtins.input", side_effect=[
    "1", "INVALID", "EXECUTED", "нет", "нет", "нет"
])
def test_invalid_inputs_handling(mock_input, capsys):
    """Тестирует обработку неверного статуса."""
    main()
    captured = capsys.readouterr()
    output = captured.out
    assert "Привет!" in output
    assert "JSON-файл" in output


def test_print_transactions_output(capsys, sample_transactions):
    """Тестирует вывод транзакций."""
    print_transactions(sample_transactions)
    captured = capsys.readouterr()
    assert "Перевод" in captured.out
    assert "Покупка" in captured.out


def test_print_empty_transactions(capsys):
    """Тестирует вывод пустого списка транзакций."""
    print_transactions([])
    captured = capsys.readouterr()
    assert "не найдено" in captured.out.lower()


@patch("builtins.input", side_effect=[
    "1", "EXECUTED", "да", "по возрастанию", "да", "да", "перевод"
])
def test_all_filters_application(mock_input, capsys):
    """Тестирует применение всех фильтров."""
    main()
    captured = capsys.readouterr()
    assert "Перевод организации" in captured.out
