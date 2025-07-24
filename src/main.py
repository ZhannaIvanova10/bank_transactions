from typing import List, Dict
import re
from collections import Counter  # Используется в process_bank_operations


def load_transactions(file_type: str) -> List[Dict]:
    """Загружает транзакции из файла указанного типа."""
    if file_type not in ("1", "2", "3"):
        print("\nОшибка: Неподдерживаемый тип файла")
        raise ValueError("Неподдерживаемый тип файла")

    return [
        {
            "description": "Перевод организации",
            "status": "EXECUTED",
            "date": "2023-01-01",
            "amount": 1000,
            "currency": "RUB"
        },
        {
            "description": "Открытие вклада",
            "status": "EXECUTED",
            "date": "2023-01-02",
            "amount": 5000,
            "currency": "RUB"
        }
    ]


def filter_by_status(
        transactions: List[Dict],
        status: str
) -> List[Dict]:
    """Фильтрует транзакции по статусу."""
    return [
        tx for tx in transactions
        if tx.get('status', '').upper() == status.upper()
    ]


def filter_by_currency(
        transactions: List[Dict],
        currency: str
) -> List[Dict]:
    """Фильтрует транзакции по валюте."""
    return [
        tx for tx in transactions
        if tx.get('currency', '').upper() == currency.upper()
    ]


def sort_transactions(
        transactions: List[Dict],
        reverse: bool = False
) -> List[Dict]:
    """Сортирует транзакции по дате."""
    return sorted(
        transactions,
        key=lambda x: x.get('date', ''),
        reverse=reverse
    )


def process_bank_search(
        data: List[Dict],
        search: str
) -> List[Dict]:
    """Ищет транзакции по строке в описании."""
    pattern = re.compile(search, re.IGNORECASE)
    return [tx for tx in data if pattern.search(tx.get('description', ''))]


def process_bank_operations(
        data: List[Dict],
        categories: List[str]
) -> Dict[str, int]:
    """Подсчитывает количество операций по заданным категориям."""
    descriptions = [tx.get('description', '') for tx in data]
    counter = Counter(desc for desc in descriptions if desc in categories)
    return dict(counter)


def print_transactions(transactions: List[Dict]):
    """Выводит транзакции в консоль."""
    if not transactions:
        msg = "Не найдено ни одной транзакции, "
        msg += "подходящей под ваши условия"
        print(msg)
        return

    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")
    for tx in transactions:
        print(f"{tx.get('date')} {tx.get('description')}")
        print(f"Сумма: {tx.get('amount')} {tx.get('currency')}\n")


def main():
    """Основная функция программы для работы с банковскими транзакциями."""
    welcome_msg = "Привет! Добро пожаловать в программу работы "
    print(f"{welcome_msg}с банковскими транзакциями.")

    menu = (
        "Выберите необходимый пункт меню:\n"
        "1. Получить информацию о транзакциях из JSON-файла\n"
        "2. Получить информацию о транзакциях из CSV-файла\n"
        "3. Получить информацию о транзакциях из XLSX-файла\n"
    )
    file_type = input(menu)

    file_types = {"1": "JSON", "2": "CSV", "3": "XLSX"}
    file_msg = "\nДля обработки выбран "
    file_msg += f"{file_types.get(file_type, 'неизвестный')}-файл."
    print(file_msg)

    transactions = load_transactions(file_type)

    status_prompt = (
        "\nВведите статус, по которому необходимо выполнить фильтрацию.\n"
        "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
    )
    while True:
        status = input(status_prompt).upper()
        if status in ["EXECUTED", "CANCELED", "PENDING"]:
            break
        print(f'Статус операции "{status}" недоступен.')

    filtered = filter_by_status(transactions, status)
    status_msg = f"\nОперации отфильтрованы по статусу \"{status}\""
    print(status_msg)

    sort_msg = "\nОтсортировать операции по дате? Да/Нет\n"
    sort_choice = input(sort_msg).lower()
    if sort_choice == 'да':
        order_msg = "Отсортировать по возрастанию или по убыванию?\n"
        order = input(order_msg).lower()
        reverse = order == 'по убыванию'
        filtered = sort_transactions(filtered, reverse)

    currency_msg = "\nВыводить только рублевые транзакции? Да/Нет\n"
    currency_choice = input(currency_msg).lower()
    if currency_choice == 'да':
        filtered = filter_by_currency(filtered, "RUB")

    search_msg = "\nОтфильтровать список транзакций по "
    search_msg += "определенному слову в описании? Да/Нет\n"
    search_choice = input(search_msg).lower()
    if search_choice == 'да':
        search_word = input("Введите слово для поиска в описании:\n")
        filtered = process_bank_search(filtered, search_word)

    print("\nРаспечатываю итоговый список транзакций...")
    print_transactions(filtered)


if __name__ == "__main__":
    main()
