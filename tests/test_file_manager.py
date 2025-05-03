import os
from pathlib import Path
from typing import Any, Dict, List, Type

import pytest

from src.file_manager import CSVFileManager, FileManager, JSONFileManager

# --- Тесты для JSONFileManager ---


def test_json_file_manager_add_vacancy(json_file_manager: JSONFileManager) -> None:
    """Тест добавления вакансии в JSON-файл."""
    vacancy = {"title": "Test Vacancy", "url": "test_url"}
    json_file_manager.add_vacancy(vacancy)
    vacancies = json_file_manager.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0]["title"] == "Test Vacancy"


def test_json_file_manager_add_duplicate_vacancy(json_file_manager: JSONFileManager) -> None:
    """Тест добавления дублирующейся вакансии в JSON-файл."""
    vacancy = {"title": "Test Vacancy", "url": "test_url"}
    json_file_manager.add_vacancy(vacancy)
    json_file_manager.add_vacancy(vacancy)
    vacancies = json_file_manager.get_vacancies()
    assert len(vacancies) == 1  # Убеждаемся, что дубликат не добавлен


def test_json_file_manager_get_vacancies(json_file_manager: JSONFileManager) -> None:
    """Тест получения вакансий из JSON-файла."""
    vacancy1 = {"title": "Test Vacancy 1", "url": "test_url_1"}
    vacancy2 = {"title": "Test Vacancy 2", "url": "test_url_2"}
    json_file_manager.add_vacancy(vacancy1)
    json_file_manager.add_vacancy(vacancy2)
    vacancies = json_file_manager.get_vacancies()
    assert len(vacancies) == 2
    assert vacancies[0]["title"] == "Test Vacancy 1"
    assert vacancies[1]["title"] == "Test Vacancy 2"


def test_json_file_manager_delete_vacancy(json_file_manager: JSONFileManager) -> None:
    """Тест удаления вакансии из JSON-файла."""
    vacancy1 = {"title": "Test Vacancy 1", "url": "test_url_1"}
    vacancy2 = {"title": "Test Vacancy 2", "url": "test_url_2"}
    json_file_manager.add_vacancy(vacancy1)
    json_file_manager.add_vacancy(vacancy2)
    json_file_manager.delete_vacancy("test_url_1")
    vacancies = json_file_manager.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0]["title"] == "Test Vacancy 2"


def test_json_file_manager_delete_nonexistent_vacancy(json_file_manager: JSONFileManager) -> None:
    """Тест удаления несуществующей вакансии из JSON-файла."""
    vacancy = {"title": "Test Vacancy", "url": "test_url"}
    json_file_manager.add_vacancy(vacancy)
    json_file_manager.delete_vacancy("nonexistent_url")
    vacancies = json_file_manager.get_vacancies()
    assert len(vacancies) == 1


def test_json_file_manager_clear_file(json_file_manager: JSONFileManager) -> None:
    """Тест очистки JSON-файла."""
    vacancy = {"title": "Test Vacancy", "url": "test_url"}
    json_file_manager.add_vacancy(vacancy)
    json_file_manager.clear_file()
    vacancies = json_file_manager.get_vacancies()
    assert len(vacancies) == 0


def test_json_file_manager_file_not_found(json_file_manager: JSONFileManager) -> None:
    """Тест обработки FileNotFoundError в JSONFileManager."""
    # Получаем имя файла
    filename: str = json_file_manager.filename

    # Удаляем файл, чтобы вызвать FileNotFoundError
    if os.path.exists(filename):
        os.remove(filename)

    vacancies: List[Dict[str, Any]] = json_file_manager.get_vacancies()
    assert vacancies == []


def test_json_file_manager_json_decode_error(json_file_manager: JSONFileManager) -> None:
    """Тест обработки JSONDecodeError в JSONFileManager."""
    # Получаем имя файла
    filename: str = json_file_manager.filename  # Используем открытый атрибут filename

    # Создаем файл с некорректным JSON
    with open(filename, "w", encoding="utf-8") as f:
        f.write("invalid json")

    vacancies: List[Dict[str, Any]] = json_file_manager.get_vacancies()
    assert vacancies == []


# --- Тесты для CSVFileManager ---


def test_csv_file_manager_add_vacancy(csv_file_manager: CSVFileManager) -> None:
    """Тест добавления вакансии в CSV-файл."""
    vacancy = {"title": "Test Vacancy", "url": "test_url"}
    csv_file_manager.add_vacancy(vacancy)
    vacancies = csv_file_manager.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0]["title"] == "Test Vacancy"


def test_csv_file_manager_add_duplicate_vacancy(csv_file_manager: CSVFileManager) -> None:
    """Тест добавления дублирующейся вакансии в CSV-файл."""
    vacancy = {"title": "Test Vacancy", "url": "test_url"}
    csv_file_manager.add_vacancy(vacancy)
    csv_file_manager.add_vacancy(vacancy)
    vacancies = csv_file_manager.get_vacancies()
    assert len(vacancies) == 1  # Убеждаемся, что дубликат не добавлен


def test_csv_file_manager_get_vacancies(csv_file_manager: CSVFileManager) -> None:
    """Тест получения вакансий из CSV-файла."""
    vacancy1 = {"title": "Test Vacancy 1", "url": "test_url_1"}
    vacancy2 = {"title": "Test Vacancy 2", "url": "test_url_2"}
    csv_file_manager.add_vacancy(vacancy1)
    csv_file_manager.add_vacancy(vacancy2)
    vacancies = csv_file_manager.get_vacancies()
    assert len(vacancies) == 2
    assert vacancies[0]["title"] == "Test Vacancy 1"
    assert vacancies[1]["title"] == "Test Vacancy 2"


def test_csv_file_manager_delete_vacancy(csv_file_manager: CSVFileManager) -> None:
    """Тест удаления вакансии из CSV-файла."""
    vacancy1 = {"title": "Test Vacancy 1", "url": "test_url_1"}
    vacancy2 = {"title": "Test Vacancy 2", "url": "test_url_2"}
    csv_file_manager.add_vacancy(vacancy1)
    csv_file_manager.add_vacancy(vacancy2)
    csv_file_manager.delete_vacancy("test_url_1")
    vacancies = csv_file_manager.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0]["title"] == "Test Vacancy 2"


def test_csv_file_manager_delete_nonexistent_vacancy(csv_file_manager: CSVFileManager) -> None:
    """Тест удаления несуществующей вакансии из CSV-файла."""
    vacancy = {"title": "Test Vacancy", "url": "test_url"}
    csv_file_manager.add_vacancy(vacancy)
    csv_file_manager.delete_vacancy("nonexistent_url")
    vacancies = csv_file_manager.get_vacancies()
    assert len(vacancies) == 1


def test_csv_file_manager_clear_file(csv_file_manager: CSVFileManager) -> None:
    """Тест очистки CSV-файла."""
    vacancy = {"title": "Test Vacancy", "url": "test_url"}
    csv_file_manager.add_vacancy(vacancy)
    csv_file_manager.clear_file()
    vacancies = csv_file_manager.get_vacancies()
    assert len(vacancies) == 0


def test_csv_file_manager_file_not_found(csv_file_manager: CSVFileManager) -> None:
    """Тест обработки FileNotFoundError в CSVFileManager."""
    # Получаем имя файла
    filename: str = csv_file_manager.filename

    # Удаляем файл, чтобы вызвать FileNotFoundError
    if os.path.exists(filename):
        os.remove(filename)

    vacancies: List[Dict[str, Any]] = csv_file_manager.get_vacancies()
    assert vacancies == []


# --- Параметризованные тесты ---


@pytest.mark.parametrize(
    "filename, file_manager_class",
    [
        ("test_vacancies.json", JSONFileManager),
        ("test_vacancies.csv", CSVFileManager),
    ],
)
def test_file_manager_creation(tmpdir: Path, filename: str, file_manager_class: Type[FileManager]) -> None:
    """Тест создания объектов FileManager."""
    file_path = Path(tmpdir).joinpath(filename)  # Path должен быть Path-объектом
    file_manager = file_manager_class(str(file_path))  # type: ignore
    assert isinstance(file_manager, (JSONFileManager, CSVFileManager))
