import abc
import csv
import json
from typing import Any, Dict, List


class FileManager(abc.ABC):
    """Абстрактный класс для работы с файлами, содержащими информацию о вакансиях."""

    @abc.abstractmethod
    def get_vacancies(self) -> List[Dict]:
        """Получает данные из файла."""
        pass

    @abc.abstractmethod
    def add_vacancy(self, vacancy: Dict) -> None:
        """Добавляет вакансию в файл."""
        pass

    @abc.abstractmethod
    def delete_vacancy(self, vacancy_id: str) -> None:
        """Удаляет информацию о вакансии из файла."""
        pass

    @abc.abstractmethod
    def clear_file(self) -> None:
        """Очищает данные в файле"""
        pass


class JSONFileManager(FileManager):
    """Класс для сохранения информации о вакансиях в JSON-файл."""

    def __init__(self, filename: str = "vacancies.json"):
        """Инициализация объекта JSONFileManager."""
        self.__filename = filename

    @property
    def filename(self) -> str:
        return self.__filename

    def get_vacancies(self) -> List[Dict[str, Any]]:
        """Получает данные из JSON-файла."""
        try:
            with open(self.__filename, "r", encoding="utf-8") as f:
                data: List[Dict[str, Any]] = json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:  # Обработка случая поврежденного JSON
            return []
        return data

    def add_vacancy(self, vacancy: Dict) -> None:
        """Добавляет вакансию в JSON-файл, не допуская дублирования."""
        existing_vacancies = self.get_vacancies()
        if vacancy not in existing_vacancies:  # Проверка на дублирование
            existing_vacancies.append(vacancy)
            with open(self.__filename, "w", encoding="utf-8") as f:  # Указываем encoding='utf-8'
                json.dump(existing_vacancies, f, indent=4, ensure_ascii=False)

    def delete_vacancy(self, vacancy_id: str) -> None:
        """Удаляет информацию о вакансии из JSON-файла."""
        vacancies = self.get_vacancies()
        updated_vacancies = [v for v in vacancies if v.get("url") != vacancy_id]
        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump(updated_vacancies, f, indent=4, ensure_ascii=False)

    def clear_file(self) -> None:
        """Полностью очищает JSON-файл с данными."""
        with open(self.__filename, "w") as f:
            json.dump([], f)

    # Методы для БД (заглушки)
    def get_by_id(self, vacancy_id: str) -> None:
        pass

    def update(self, vacancy_id: str) -> None:
        pass


class CSVFileManager(FileManager):
    """Класс для сохранения информации о вакансиях в CSV-файл."""

    def __init__(self, filename: str = "vacancies.csv"):
        """Инициализация объекта CSVFileManager."""
        self.__filename = filename

    @property
    def filename(self) -> str:
        return self.__filename

    def get_vacancies(self) -> List[Dict]:
        """Получает данные из CSV-файла."""
        try:
            with open(self.__filename, "r", newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                return list(reader)
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Ошибка чтения из CSV-файла: {e}")
            return []

    def add_vacancy(self, vacancy: Dict) -> None:
        """Добавляет вакансию в CSV-файл."""
        vacancies = self.get_vacancies()
        if vacancy not in vacancies:  # Проверка на дублирование
            vacancies.append(vacancy)
            fieldnames = vacancy.keys()
            try:
                with open(self.__filename, "w", newline="", encoding="utf-8") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()  # Запись заголовков
                    writer.writerows(vacancies)
            except Exception as e:
                print(f"Ошибка записи CSV-файла: {e}")

    def delete_vacancy(self, vacancy_id: str) -> None:
        """Удаляет информацию о вакансии из CSV-файла."""
        vacancies = self.get_vacancies()
        updated_vacancies = [v for v in vacancies if v.get("url") != vacancy_id]
        fieldnames = vacancies[0].keys() if vacancies else []
        try:
            with open(self.__filename, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()  # Запись заголовков
                writer.writerows(updated_vacancies)
        except Exception as e:
            print(f"Ошибка записи из CSV-файла: {e}")

    def clear_file(self) -> None:
        """Полностью очищает CSV-файл с данными."""
        try:
            with open(self.__filename, "w", newline="", encoding="utf-8") as csvfile:
                csvfile.truncate(0)  # Сократите файл до 0 байт
        except Exception as e:
            print(f"Ошибка при очистке CSV-файла: {e}")
