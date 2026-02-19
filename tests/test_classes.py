"""Модульные тесты для классов артефактов."""
import unittest
import sys
import os

# Добавляем путь к родительской папке для импорта модулей
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classes import Artifact, Aphorism, Proverb


class TestArtifactCreation(unittest.TestCase):
    """Тесты для фабричного метода создания артефактов."""
    
    def test_create_aphorism_success(self):
        """Тест успешного создания афоризма."""
        aphorism = Artifact.create(
            "APHORISM", 
            content="Жизнь — это движение", 
            author="Аристотель"
        )
        
        self.assertIsInstance(aphorism, Aphorism)
        self.assertEqual(aphorism.content, "Жизнь — это движение")
        self.assertEqual(aphorism.author, "Аристотель")
        self.assertEqual(aphorism.type_name(), "APHORISM")
    
    def test_create_proverb_success(self):
        """Тест успешного создания пословицы."""
        proverb = Artifact.create(
            "PROVERB", 
            content="Без труда не выловишь и рыбку из пруда", 
            country="Россия"
        )
        
        self.assertIsInstance(proverb, Proverb)
        self.assertEqual(proverb.content, "Без труда не выловишь и рыбку из пруда")
        self.assertEqual(proverb.country, "Россия")
        self.assertEqual(proverb.type_name(), "PROVERB")
    
    def test_create_unknown_type(self):
        """Тест создания артефакта неизвестного типа."""
        with self.assertRaises(ValueError) as context:
            Artifact.create("UNKNOWN", content="test", author="test")
        
        self.assertEqual(str(context.exception), "Неизвестный тип: UNKNOWN")
    
    def test_create_aphorism_missing_author(self):
        """Тест создания афоризма без обязательного поля author."""
        with self.assertRaises(KeyError):
            Artifact.create("APHORISM", content="test")
    
    def test_create_proverb_missing_country(self):
        """Тест создания пословицы без обязательного поля country."""
        with self.assertRaises(KeyError):
            Artifact.create("PROVERB", content="test")


class TestAphorism(unittest.TestCase):
    """Тесты для класса Aphorism."""
    
    def setUp(self):
        """Подготовка данных перед каждым тестом."""
        self.aphorism = Aphorism(
            content="Знание — сила", 
            author="Фрэнсис Бэкон"
        )
    
    def test_aphorism_attributes(self):
        """Тест атрибутов афоризма."""
        self.assertEqual(self.aphorism.content, "Знание — сила")
        self.assertEqual(self.aphorism.author, "Фрэнсис Бэкон")
        self.assertEqual(self.aphorism.type_name(), "APHORISM")
    
    def test_matches_condition_content_true(self):
        """Тест проверки условия для content (позитивный)."""
        result = self.aphorism.matches_condition("content", "сила")
        self.assertTrue(result)
    
    def test_matches_condition_content_false(self):
        """Тест проверки условия для content (негативный)."""
        result = self.aphorism.matches_condition("content", "мудрость")
        self.assertFalse(result)
    
    def test_matches_condition_author_true(self):
        """Тест проверки условия для author (позитивный)."""
        result = self.aphorism.matches_condition("author", "Бэкон")
        self.assertTrue(result)
    
    def test_matches_condition_author_false(self):
        """Тест проверки условия для author (негативный)."""
        result = self.aphorism.matches_condition("author", "Сократ")
        self.assertFalse(result)
    
    def test_matches_condition_nonexistent_attr(self):
        """Тест проверки условия для несуществующего атрибута."""
        result = self.aphorism.matches_condition("nonexistent", "test")
        self.assertFalse(result)
    
    def test_str_representation(self):
        """Тест строкового представления афоризма."""
        expected = '[APHORISM] content="Знание — сила" author="Фрэнсис Бэкон"'
        self.assertEqual(str(self.aphorism), expected)


class TestProverb(unittest.TestCase):
    """Тесты для класса Proverb."""
    
    def setUp(self):
        """Подготовка данных перед каждым тестом."""
        self.proverb = Proverb(
            content="В гостях хорошо, а дома лучше", 
            country="Россия"
        )
    
    def test_proverb_attributes(self):
        """Тест атрибутов пословицы."""
        self.assertEqual(self.proverb.content, "В гостях хорошо, а дома лучше")
        self.assertEqual(self.proverb.country, "Россия")
        self.assertEqual(self.proverb.type_name(), "PROVERB")
    
    def test_matches_condition_content_true(self):
        """Тест проверки условия для content (позитивный)."""
        result = self.proverb.matches_condition("content", "гостях")
        self.assertTrue(result)
    
    def test_matches_condition_content_false(self):
        """Тест проверки условия для content (негативный)."""
        result = self.proverb.matches_condition("content", "работа")
        self.assertFalse(result)
    
    def test_matches_condition_country_true(self):
        """Тест проверки условия для country (позитивный)."""
        result = self.proverb.matches_condition("country", "Рос")
        self.assertTrue(result)
    
    def test_matches_condition_country_false(self):
        """Тест проверки условия для country (негативный)."""
        result = self.proverb.matches_condition("country", "Англия")
        self.assertFalse(result)
    
    def test_str_representation(self):
        """Тест строкового представления пословицы."""
        expected = '[PROVERB] content="В гостях хорошо, а дома лучше" country="Россия"'
        self.assertEqual(str(self.proverb), expected)


if __name__ == '__main__':
    unittest.main()