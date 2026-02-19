"""Точка входа в программу. Запускает обработку файла с командами."""
from comand_parser import CommandProcessor

def main():
    """Главная функция для запуска программы."""
    cp = CommandProcessor()
    cp.execute_file("artifact.txt")

if __name__ == "__main__":
    main()
