"""Модуль с классами артефактов (афоризмы и пословицы)."""
from abc import ABC, abstractmethod

class Artifact(ABC):
    """Абстрактный базовый класс для всех артефактов."""
    def __init__(self, content: str):
        self.content = content

    @staticmethod
    def create(type_name: str, **kwargs):
        """Фабричный метод создания артефактов."""
        if type_name == "APHORISM":
            return Aphorism(content=kwargs["content"], author=kwargs["author"])
        if type_name == "PROVERB":
            return Proverb(content=kwargs["content"], country=kwargs["country"])
        raise ValueError(f"Неизвестный тип: {type_name}")

    #метод который обязан релизовать класс наследник для возрата типа (aphorism, proverb)
    @abstractmethod
    def type_name(self):
        """Возвращает название типа объекта."""

    # метод который обязан релизовать класс наследник
    # для сверки и возвращения content/author/country
    @abstractmethod
    def matches_condition(self, attr, value):
        """Проверка условия для REM"""

    #для преобразования контента объекта в строку
    def __str__(self):
        return f"[{self.type_name()}] content=\"{self.content}\""


class Aphorism(Artifact):
    """Класс афоризма. Содержит текст и автора."""
    def __init__(self, content: str, author: str):
        super().__init__(content)
        self.author = author

    def type_name(self):
        return "APHORISM"

    def matches_condition(self, attr, value):
        """Универсальная проверка условия."""
        if hasattr(self, attr):
            return value in str(getattr(self, attr))
        return False

    def __str__(self):
        return f"[APHORISM] content=\"{self.content}\" author=\"{self.author}\""


class Proverb(Artifact):
    """Класс пословицы. Содержит текст и страну происхождения."""
    def __init__(self, content: str, country: str):
        super().__init__(content)
        self.country = country

    def type_name(self):
        return "PROVERB"

    def matches_condition(self, attr, value):
        """Универсальная проверка условия."""
        if hasattr(self, attr):
            return value in str(getattr(self, attr))
        return False

    def __str__(self):
        return f"[PROVERB] content=\"{self.content}\" country=\"{self.country}\""
