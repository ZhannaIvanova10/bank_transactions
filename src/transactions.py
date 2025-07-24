import re
from collections import Counter
from typing import List, Dict


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """Ищет транзакции по строке в описании с использованием regex."""
    try:
        pattern = re.compile(search, re.IGNORECASE)
        return [
            tx for tx in data
            if 'description' in tx and pattern.search(tx['description'])
        ]
    except re.error:
        return []


def process_bank_operations(
        data: List[Dict],
        categories: List[str]
) -> Dict[str, int]:
    """Подсчитывает количество транзакций по заданным категориям."""
    descriptions = []
    for tx in data:
        desc = tx.get('description', '')
        descriptions.append(str(desc).lower() if desc is not None else '')

    category_counts = Counter(descriptions)
    return {
        cat: category_counts.get(cat.lower(), 0)
        for cat in categories
    }
