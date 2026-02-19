"""Модуль для парсинга команд из файла и их выполнения."""
from classes import Artifact
from repository import Repository


class CommandProcessor:
    """Класс для обработки команд из файла (ADD, REM, PRINT)."""
    def __init__(self):
        #создаем компазицию, когда CP будет внутри содержать Repo
        self.repo = Repository()


    def process_line(self, line: str) -> None:
        """Обрабатывает строку команды."""
        #чистим от пробелов
        line = line.strip()
        if not line:
            return None #!!

        #Проверяем начало строки на команду при помощи startswith
        #берем строку от 5 символа, чистим от пробелов и вызываем нужный метод.

        # ADD команда
        if line.startswith("ADD"):
            return self.process_add(line[4:].strip())

        # REM content~"text"
        if line.startswith("REM"):
            return self.process_rem(line[4:].strip())

        # PRINT - просто вызываем сразу метод вывода из репозитория
        if line == "PRINT":
            return self.repo.print_all()
            
        print("Недопустимая команда в файле:", line)

    def parse_args(self, arg_string: str):
        """Парсит строку аргументов вида key="value";key2="value2" в словарь."""
        result = {}
        parts = arg_string.split(";")
        for part in parts:
            if "=" in part:
                key, val = part.split("=", 1)
                #убираем пробелы и кавычки
                result[key.strip()] = val.strip().strip("\"")
        return result

    #смотрим на тип команды, создаем на ее основе объект класса.
    def process_add(self, data: str):
        """Обрабатывает команду ADD, создавая объект и добавляя его в репозиторий."""
        #разбиваем строку APHORISM;content="Жизнь — это движение";author="Аристотель"
        #на два, тип фразы отпраляем в type_name
        #аргументы цельной строкой отправляем в args
        if ";" not in data:
            print(f"Ошибка в команде ADD: отсутствует точка с запятой в '{data}'")
            return
            
        type_name, args = data.split(";", 1)

        #делаем из аргементов кортеж
        args = self.parse_args(args)

        try:
            obj = Artifact.create(type_name, **args)
            self.repo.add(obj)
        except KeyError as e:
            print(f"Ошибка: отсутствует обязательный параметр {e} для типа {type_name}")
        except ValueError as e:
            print(e)

    #делим строку на аттрибут и значение, очищаем от пробелов и кавычек
    #значение, вызываем remove_by_condition
    def process_rem(self, data: str):
        """Обрабатывает команду REM, удаляя объекты из репозитория по условию."""
        # пример: content~"abc"
        if "~" not in data:
            print(f"Ошибка в команде REM: отсутствует символ '~' в '{data}'")
            return
            
        try:
            attr, value = data.split("~", 1)
            value = value.strip().strip("\"")
            self.repo.remove_by_condition(attr, value)
        except Exception as e:
            print(f"Ошибка при обработке команды REM '{data}': {e}")

    def execute_file(self, filename: str) -> None:
        """Читает команды из файла и выполняет их."""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    self.process_line(line)
        except FileNotFoundError:
            print(f"Файл {filename} не найден")
            raise