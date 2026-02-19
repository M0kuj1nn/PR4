"""Модуль для хранения и управления коллекцией артефактов."""
from typing import List
from classes import Artifact

class Repository:
    """Класс-контейнер для хранения и управления артефактами."""
    def __init__(self):
        """Инициализирует пустой репозиторий."""
        self.items: List[Artifact] = []

    def add(self, item: Artifact) -> None:
        """Добавляет артефакт в репозиторий."""
        self.items.append(item)

    def remove_by_condition(self, attr: str, value: str) -> None:
        """Удаляет артефакты, которые соответствуют условию attr~value."""
        self.items = [
            i for i in self.items
            if not i.matches_condition(attr, value)
        ]

    def print_all(self) -> None:
        """Выводит все артефакты из репозитория."""
        for item in self.items:
            print(item)
