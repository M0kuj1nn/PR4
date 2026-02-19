"""Модульные тесты для класса CommandProcessor."""
import unittest
import sys
import os
import tempfile
from io import StringIO
from contextlib import redirect_stdout

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from comand_parser import CommandProcessor
from classes import Aphorism, Proverb


class TestCommandProcessor(unittest.TestCase):
    """Тесты для класса CommandProcessor."""
    
    def setUp(self):
        """Подготовка данных перед каждым тестом."""
        self.processor = CommandProcessor()
    
    def test_parse_args_single(self):
        """Тест парсинга одного аргумента."""
        args_str = 'content="Жизнь — это движение"'
        result = self.processor.parse_args(args_str)
        
        expected = {"content": "Жизнь — это движение"}
        self.assertEqual(result, expected)
    
    def test_parse_args_multiple(self):
        """Тест парсинга нескольких аргументов."""
        args_str = 'content="Жизнь — это движение";author="Аристотель"'
        result = self.processor.parse_args(args_str)
        
        expected = {
            "content": "Жизнь — это движение",
            "author": "Аристотель"
        }
        self.assertEqual(result, expected)
    
    def test_parse_args_with_spaces(self):
        """Тест парсинга аргументов с пробелами."""
        args_str = '  content  =  "Текст с пробелами"  ;  author  =  "Автор"  '
        result = self.processor.parse_args(args_str)
        
        expected = {
            "content": "Текст с пробелами",
            "author": "Автор"
        }
        self.assertEqual(result, expected)
    
    def test_parse_args_empty(self):
        """Тест парсинга пустой строки."""
        result = self.processor.parse_args("")
        self.assertEqual(result, {})
    
    def test_parse_args_invalid_format(self):
        """Тест парсинга строки с неверным форматом."""
        # Строка без знака "=" должна игнорироваться
        result = self.processor.parse_args("content:test")
        self.assertEqual(result, {})
    
    def test_process_add_aphorism(self):
        """Тест обработки команды ADD для афоризма."""
        line = 'ADD APHORISM;content="Знание — сила";author="Фрэнсис Бэкон"'
        self.processor.process_line(line)
        
        self.assertEqual(len(self.processor.repo.items), 1)
        item = self.processor.repo.items[0]
        self.assertIsInstance(item, Aphorism)
        self.assertEqual(item.content, "Знание — сила")
        self.assertEqual(item.author, "Фрэнсис Бэкон")
    
    def test_process_add_proverb(self):
        """Тест обработки команды ADD для пословицы."""
        line = 'ADD PROVERB;content="Без труда не выловишь и рыбку из пруда";country="Россия"'
        self.processor.process_line(line)
        
        self.assertEqual(len(self.processor.repo.items), 1)
        item = self.processor.repo.items[0]
        self.assertIsInstance(item, Proverb)
        self.assertEqual(item.content, "Без труда не выловишь и рыбку из пруда")
        self.assertEqual(item.country, "Россия")
    
    def test_process_add_invalid_type(self):
        """Тест обработки команды ADD с неверным типом."""
        line = 'ADD UNKNOWN;content="test";author="test"'
        
        # Перехватываем вывод ошибки
        f = StringIO()
        with redirect_stdout(f):
            self.processor.process_line(line)
        
        self.assertEqual(len(self.processor.repo.items), 0)
        output = f.getvalue().strip()
        self.assertIn("Неизвестный тип: UNKNOWN", output)
    
    def test_process_add_missing_args(self):
        """Тест обработки команды ADD с отсутствующими аргументами."""
        line = 'ADD APHORISM;content="test"'  # Нет author
        
        # Перехватываем вывод
        f = StringIO()
        with redirect_stdout(f):
            self.processor.process_line(line)
        
        output = f.getvalue().strip()
        # Проверяем, что появилось сообщение об ошибке
        self.assertIn("Ошибка: отсутствует обязательный параметр", output)
        self.assertIn("'author'", output)
        # Проверяем, что объект НЕ добавился
        self.assertEqual(len(self.processor.repo.items), 0)
    
    def test_process_rem_by_content(self):
        """Тест обработки команды REM по content."""
        # Добавляем элементы
        self.processor.process_line('ADD APHORISM;content="Знание — сила";author="Фрэнсис Бэкон"')
        self.processor.process_line('ADD APHORISM;content="Мыслю, следовательно существую";author="Рене Декарт"')
        
        # Удаляем по условию
        self.processor.process_line('REM content~"сила"')
        
        self.assertEqual(len(self.processor.repo.items), 1)
        self.assertEqual(self.processor.repo.items[0].content, "Мыслю, следовательно существую")
    
    def test_process_rem_by_author(self):
        """Тест обработки команды REM по author."""
        self.processor.process_line('ADD APHORISM;content="Знание — сила";author="Фрэнсис Бэкон"')
        self.processor.process_line('ADD APHORISM;content="Мыслю, следовательно существую";author="Рене Декарт"')
        
        self.processor.process_line('REM author~"Бэкон"')
        
        self.assertEqual(len(self.processor.repo.items), 1)
        self.assertEqual(self.processor.repo.items[0].author, "Рене Декарт")
    
    def test_process_rem_by_country(self):
        """Тест обработки команды REM по country."""
        self.processor.process_line('ADD PROVERB;content="Без труда...";country="Россия"')
        self.processor.process_line('ADD PROVERB;content="When in Rome...";country="Англия"')
        
        self.processor.process_line('REM country~"Рос"')
        
        self.assertEqual(len(self.processor.repo.items), 1)
        self.assertEqual(self.processor.repo.items[0].country, "Англия")
    
    def test_process_rem_invalid_format(self):
        """Тест обработки команды REM с неверным форматом."""
        line = 'REM content="test"'  # Должно быть ~, а не =
        
        # Перехватываем вывод
        f = StringIO()
        with redirect_stdout(f):
            self.processor.process_line(line)
        
        output = f.getvalue().strip()
        # Проверяем, что появилось сообщение об ошибке
        self.assertIn("Ошибка в команде REM: отсутствует символ '~'", output)
    
    def test_process_print(self):
        """Тест обработки команды PRINT."""
        self.processor.process_line('ADD APHORISM;content="Знание — сила";author="Фрэнсис Бэкон"')
        
        f = StringIO()
        with redirect_stdout(f):
            self.processor.process_line('PRINT')
        
        output = f.getvalue().strip()
        self.assertIn("Знание — сила", output)
        self.assertIn("Фрэнсис Бэкон", output)
    
    def test_process_empty_line(self):
        """Тест обработки пустой строки."""
        result = self.processor.process_line("")
        self.assertIsNone(result)
    
    def test_process_invalid_command(self):
        """Тест обработки неверной команды."""
        f = StringIO()
        with redirect_stdout(f):
            self.processor.process_line("INVALID command")
        
        output = f.getvalue().strip()
        self.assertIn("Недопустимая команда в файле: INVALID command", output)
    
    def test_execute_file(self):
        """Тест выполнения команд из файла."""
        # Создаем временный файл с командами
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
            f.write('ADD APHORISM;content="Знание — сила";author="Фрэнсис Бэкон"\n')
            f.write('ADD PROVERB;content="Без труда...";country="Россия"\n')
            f.write('PRINT\n')
            f.write('REM content~"сила"\n')
            f.write('PRINT\n')
            temp_filename = f.name
        
        try:
            # Перехватываем вывод
            f = StringIO()
            with redirect_stdout(f):
                self.processor.execute_file(temp_filename)
            
            output = f.getvalue()
            self.assertIn("Знание — сила", output)
            self.assertIn("Без труда", output)
            
            # После удаления должен остаться только один элемент
            self.assertEqual(len(self.processor.repo.items), 1)
            self.assertEqual(self.processor.repo.items[0].content, "Без труда...")
            
        finally:
            # Удаляем временный файл
            os.unlink(temp_filename)
    
    def test_execute_file_not_found(self):
        """Тест выполнения команд из несуществующего файла."""
        with self.assertRaises(FileNotFoundError):
            self.processor.execute_file("nonexistent_file.txt")


if __name__ == '__main__':
    unittest.main()