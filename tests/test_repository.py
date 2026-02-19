"""Модульные тесты для класса Repository."""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from repository import Repository
from classes import Aphorism, Proverb


class TestRepository(unittest.TestCase):
    """Тесты для класса Repository."""
    
    def setUp(self):
        """Подготовка данных перед каждым тестом."""
        self.repo = Repository()
        
        self.aphorism1 = Aphorism("Знание — сила", "Фрэнсис Бэкон")
        self.aphorism2 = Aphorism("Мыслю, следовательно существую", "Рене Декарт")
        self.proverb1 = Proverb("Без труда не выловишь и рыбку из пруда", "Россия")
        self.proverb2 = Proverb("When in Rome, do as the Romans do", "Англия")
    
    def test_add_single_item(self):
        """Тест добавления одного элемента."""
        self.repo.add(self.aphorism1)
        
        self.assertEqual(len(self.repo.items), 1)
        self.assertIn(self.aphorism1, self.repo.items)
    
    def test_add_multiple_items(self):
        """Тест добавления нескольких элементов."""
        items = [self.aphorism1, self.aphorism2, self.proverb1]
        
        for item in items:
            self.repo.add(item)
        
        self.assertEqual(len(self.repo.items), 3)
        for item in items:
            self.assertIn(item, self.repo.items)
    
    def test_remove_by_condition_content(self):
        """Тест удаления по условию для content."""
        # Добавляем элементы
        self.repo.add(self.aphorism1)
        self.repo.add(self.aphorism2)
        self.repo.add(self.proverb1)
        self.repo.add(self.proverb2)
        
        # Удаляем элементы, содержащие "сила" в content
        self.repo.remove_by_condition("content", "сила")
        
        self.assertEqual(len(self.repo.items), 3)
        self.assertNotIn(self.aphorism1, self.repo.items)
        self.assertIn(self.aphorism2, self.repo.items)
        self.assertIn(self.proverb1, self.repo.items)
        self.assertIn(self.proverb2, self.repo.items)
    
    def test_remove_by_condition_author(self):
        """Тест удаления по условию для author."""
        self.repo.add(self.aphorism1)
        self.repo.add(self.aphorism2)
        
        self.repo.remove_by_condition("author", "Декарт")
        
        self.assertEqual(len(self.repo.items), 1)
        self.assertIn(self.aphorism1, self.repo.items)
        self.assertNotIn(self.aphorism2, self.repo.items)
    
    def test_remove_by_condition_country(self):
        """Тест удаления по условию для country."""
        self.repo.add(self.proverb1)
        self.repo.add(self.proverb2)
        
        self.repo.remove_by_condition("country", "Рос")
        
        self.assertEqual(len(self.repo.items), 1)
        self.assertNotIn(self.proverb1, self.repo.items)
        self.assertIn(self.proverb2, self.repo.items)
    
    def test_remove_by_condition_no_matches(self):
        """Тест удаления по условию без совпадений."""
        self.repo.add(self.aphorism1)
        self.repo.add(self.proverb1)
        
        self.repo.remove_by_condition("content", "nonexistent")
        
        self.assertEqual(len(self.repo.items), 2)
    
    def test_remove_by_condition_empty_repo(self):
        """Тест удаления из пустого репозитория."""
        # Не должно вызывать ошибок
        self.repo.remove_by_condition("content", "test")
        
        self.assertEqual(len(self.repo.items), 0)
    
    def test_remove_by_condition_nonexistent_attr(self):
        """Тест удаления по несуществующему атрибуту."""
        self.repo.add(self.aphorism1)
        
        # Должно просто ничего не удалить
        self.repo.remove_by_condition("nonexistent", "test")
        
        self.assertEqual(len(self.repo.items), 1)
    
    def test_print_all(self, capsys=None):
        """Тест вывода всех элементов."""
        # Этот тест сложно автоматизировать без перехвата вывода
        # Просто проверяем, что метод не падает
        self.repo.print_all()  # Пустой вывод
        
        self.repo.add(self.aphorism1)
        self.repo.add(self.proverb1)
        
        try:
            self.repo.print_all()  # Должно работать без ошибок
        except Exception as e:
            self.fail(f"print_all вызвал исключение: {e}")


if __name__ == '__main__':
    unittest.main()