#!/usr/bin/env python3
"""Скрипт для запуска всех модульных тестов."""
import unittest
import sys
import os

if __name__ == '__main__':
    # Добавляем текущую директорию в путь
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    # Загружаем все тесты из директории tests
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Возвращаем код ошибки, если были проваленные тесты
    sys.exit(not result.wasSuccessful())