"""Интеграционные тесты для всей программы."""
import unittest
import sys
import os
import tempfile
from io import StringIO
from contextlib import redirect_stdout

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import main
from comand_parser import CommandProcessor


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты."""
    
    def test_full_workflow_with_temp_file(self):
        """Тест полного рабочего процесса с временным файлом."""
        # Создаем временный файл с командами
        commands = [
            'ADD APHORISM;content="Знание — сила";author="Фрэнсис Бэкон"',
            'ADD APHORISM;content="Мыслю, следовательно существую";author="Рене Декарт"',
            'ADD PROVERB;content="Без труда не выловишь и рыбку из пруда";country="Россия"',
            'ADD PROVERB;content="When in Rome, do as the Romans do";country="Англия"',
            'PRINT',
            'REM content~"сила"',
            'REM country~"Англ"',
            'PRINT'
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
            f.write('\n'.join(commands))
            temp_filename = f.name
        
        try:
            # Создаем процессор и выполняем команды
            processor = CommandProcessor()
            
            # Перехватываем вывод
            f = StringIO()
            with redirect_stdout(f):
                processor.execute_file(temp_filename)
            
            output = f.getvalue()
            
            # Проверяем, что все добавленные элементы были выведены
            self.assertIn("Знание — сила", output)
            self.assertIn("Фрэнсис Бэкон", output)
            self.assertIn("Мыслю, следовательно существую", output)
            self.assertIn("Рене Декарт", output)
            self.assertIn("Без труда", output)
            self.assertIn("Россия", output)
            self.assertIn("When in Rome", output)
            self.assertIn("Англия", output)
            
            # После удаления должны остаться только 2 элемента
            self.assertEqual(len(processor.repo.items), 2)
            
            # Проверяем, какие элементы остались
            contents = [item.content for item in processor.repo.items]
            self.assertIn("Мыслю, следовательно существую", contents)
            self.assertIn("Без труда не выловишь и рыбку из пруда", contents)
            
        finally:
            os.unlink(temp_filename)
    
    def test_error_handling_invalid_commands(self):
        """Тест обработки ошибок при неверных командах."""
        commands = [
            'ADD APHORISM;content="Знание — сила";author="Фрэнсис Бэкон"',
            'ADD UNKNOWN;content="test";author="test"',  # Неверный тип
            'REM invalid_format',  # Неверный формат REM (без ~)
            'INVALID COMMAND',  # Неверная команда
            'ADD PROVERB;content="Без труда..."'  # Неполные аргументы (нет country)
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
            f.write('\n'.join(commands))
            temp_filename = f.name
        
        try:
            processor = CommandProcessor()
            
            f = StringIO()
            with redirect_stdout(f):
                processor.execute_file(temp_filename)
            
            output = f.getvalue()
            print("DEBUG OUTPUT:", output)  # Для отладки
            
            # Проверяем, что все ошибки были обработаны
            self.assertIn("Неизвестный тип: UNKNOWN", output)
            self.assertIn("Ошибка в команде REM: отсутствует символ '~' в 'invalid_format'", output)
            self.assertIn("Недопустимая команда в файле: INVALID COMMAND", output)
            self.assertIn("Ошибка: отсутствует обязательный параметр 'country' для типа PROVERB", output)
            
            # Должен добавиться только первый элемент
            self.assertEqual(len(processor.repo.items), 1)
            self.assertEqual(processor.repo.items[0].content, "Знание — сила")
            
        finally:
            os.unlink(temp_filename)
    
    def test_empty_file(self):
        """Тест обработки пустого файла."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
            f.write('')
            temp_filename = f.name
        
        try:
            processor = CommandProcessor()
            
            # Не должно быть ошибок
            try:
                processor.execute_file(temp_filename)
            except Exception as e:
                self.fail(f"execute_file вызвал исключение для пустого файла: {e}")
            
            self.assertEqual(len(processor.repo.items), 0)
            
        finally:
            os.unlink(temp_filename)
    
    def test_file_with_only_comments_and_empty_lines(self):
        """Тест файла с пустыми строками."""
        commands = [
            '',  # Пустая строка
            '  ',  # Строка с пробелами
            'ADD APHORISM;content="Знание — сила";author="Фрэнсис Бэкон"',
            '',  # Пустая строка
            'ADD PROVERB;content="Без труда...";country="Россия"',
            '   ',  # Строка с пробелами
            'PRINT'
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
            f.write('\n'.join(commands))
            temp_filename = f.name
        
        try:
            processor = CommandProcessor()
            
            f = StringIO()
            with redirect_stdout(f):
                processor.execute_file(temp_filename)
            
            output = f.getvalue()
            
            # Проверяем, что все команды выполнились
            self.assertIn("Знание — сила", output)
            self.assertIn("Без труда", output)
            self.assertEqual(len(processor.repo.items), 2)
            
        finally:
            os.unlink(temp_filename)
    
    def test_main_function(self):
        """Тест функции main с временным файлом artifact.txt."""
        # Создаем временный файл с именем artifact.txt в текущей директории
        test_commands = [
            'ADD APHORISM;content="Тестовый афоризм";author="Тест Автор"',
            'ADD PROVERB;content="Тестовая пословица";country="Тест Страна"',
            'PRINT'
        ]
        
        # Сохраняем оригинальный файл, если он существует
        original_exists = os.path.exists("artifact.txt")
        original_content = None
        if original_exists:
            with open("artifact.txt", "r", encoding="utf-8") as f:
                original_content = f.read()
        
        try:
            # Создаем тестовый файл
            with open("artifact.txt", "w", encoding="utf-8") as f:
                f.write('\n'.join(test_commands))
            
            # Перехватываем вывод main
            f = StringIO()
            with redirect_stdout(f):
                main()
            
            output = f.getvalue()
            
            # Проверяем, что main отработал
            self.assertIn("Тестовый афоризм", output)
            self.assertIn("Тест Автор", output)
            self.assertIn("Тестовая пословица", output)
            self.assertIn("Тест Страна", output)
            
        finally:
            # Восстанавливаем оригинальный файл
            if original_exists:
                with open("artifact.txt", "w", encoding="utf-8") as f:
                    f.write(original_content)
            else:
                if os.path.exists("artifact.txt"):
                    os.unlink("artifact.txt")


if __name__ == '__main__':
    unittest.main()