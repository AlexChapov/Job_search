import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock, patch

import pytest

from src.utils import (
    create_vacancy_from_hh_item,
    display_vacancies,
    get_vacancies_from_hh,
    load_vacancies_from_file,
    save_vacancies_to_file,
)
from src.vacancy import Vacancy


def test_get_vacancies_from_hh_no_data(mock_hh_api: MagicMock) -> None:
    """Тест получения вакансий из hh.ru, когда нет данных."""
    mock_hh_api.return_value = None
    vacancies: List[Vacancy] = get_vacancies_from_hh("Python", "113", num_pages=1)  # Добавлен area_id
    assert len(vacancies) == 0


def test_get_vacancies_from_hh_empty_items(mock_hh_api: MagicMock) -> None:
    """Тест получения вакансий из hh.ru, когда items пустой."""
    mock_hh_api.return_value = {"items": []}
    vacancies: List[Vacancy] = get_vacancies_from_hh("Python", "113", num_pages=1)  # Добавлен area_id
    assert len(vacancies) == 0


def test_get_vacancies_from_hh_multiple_pages(
    mock_hh_api: MagicMock, sample_hh_item: Dict[str, Any], sample_vacancy: Vacancy
) -> None:
    """Тест получения вакансий из hh.ru с нескольких страниц."""
    mock_hh_api.return_value = MagicMock()
    mock_hh_api.return_value.json.return_value = MagicMock(
        side_effect=[
            {"items": [sample_hh_item]},
            {"items": [sample_hh_item]},
        ]
    )
    vacancies = get_vacancies_from_hh("Python", "113", num_pages=2)  # Добавлен area_id
    assert all(isinstance(v, Vacancy) for v in vacancies)


def test_create_vacancy_from_hh_item_success(sample_hh_item: Dict[str, Any], sample_vacancy: Vacancy) -> None:
    """Тест успешного создания объекта Vacancy из элемента hh.ru."""
    vacancy = create_vacancy_from_hh_item(sample_hh_item)
    assert isinstance(vacancy, Vacancy)
    assert vacancy.title == "Python Developer"


def test_create_vacancy_from_hh_item_missing_salary(sample_hh_item: Dict[str, Any]) -> None:
    """Тест создания объекта Vacancy, когда отсутствует информация о зарплате."""
    del sample_hh_item["salary"]
    vacancy: Optional[Vacancy] = create_vacancy_from_hh_item(sample_hh_item)

    if vacancy:
        assert vacancy.salary_from == 0
        assert vacancy.salary_to == 0
    else:
        assert False, "Vacancy should not be None"


def test_create_vacancy_from_hh_item_missing_snippet(sample_hh_item: Dict[str, Any]) -> None:
    """Тест создания объекта Vacancy, когда отсутствует snippet."""
    del sample_hh_item["snippet"]
    vacancy: Optional[Vacancy] = create_vacancy_from_hh_item(sample_hh_item)

    if vacancy:
        assert vacancy.description == ""
    else:
        assert False, "Vacancy should not be None"


def test_create_vacancy_from_hh_item_key_error(sample_hh_item: Dict[str, Any]) -> None:
    """Тест создания объекта Vacancy, когда отсутствует ключевое поле."""
    del sample_hh_item["name"]
    vacancy = create_vacancy_from_hh_item(sample_hh_item)
    assert vacancy is None


def test_display_vacancies_empty_list(capsys: pytest.CaptureFixture[str]) -> None:
    """Тест отображения вакансий, когда список пуст."""
    display_vacancies([])
    captured = capsys.readouterr()
    assert "Нет вакансий для отображения." in captured.out


def test_display_vacancies_success(capsys: pytest.CaptureFixture[str], sample_vacancy: Vacancy) -> None:
    """Тест успешного отображения вакансий."""
    display_vacancies([sample_vacancy])
    captured = capsys.readouterr()
    assert "Название: Python Developer" in captured.out
    assert "Ссылка: https://example.com/vacancy/123" in captured.out
    assert "Зарплата: 100000 - 150000" in captured.out
    assert "Описание: Python, Django Develop web applications" in captured.out


@patch("src.utils.JSONFileManager.add_vacancy")
def test_save_vacancies_to_file_success(
    mock_add_vacancy: MagicMock, sample_vacancy: Vacancy, capsys: pytest.CaptureFixture[str], tmpdir: Path
) -> None:
    """Тест успешного сохранения вакансий в файл."""
    filename: Path = tmpdir / "test_vacancies.json"  # Используйте оператор / для объединения путей
    filename_str: str = str(filename)
    save_vacancies_to_file([sample_vacancy], filename_str)  # Передайте строку, а не Path
    mock_add_vacancy.assert_called_once()
    captured = capsys.readouterr()
    assert f"Сохранено 1 вакансий в {filename_str}" in captured.out


@patch("src.utils.JSONFileManager.get_vacancies")
def test_load_vacancies_from_file_success(mock_get_vacancies: MagicMock, sample_vacancy: Dict[str, Any]) -> None:
    """Тест успешной загрузки вакансий из файла."""
    mock_get_vacancies.return_value = [dict(sample_vacancy)]
    vacancies = load_vacancies_from_file("test_vacancies.json")
    assert len(vacancies) == 1
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].title == "Python Developer"


def test_load_vacancies_from_file_empty_file(tmpdir: Path) -> None:
    """Тест загрузки вакансий из пустого файла."""
    filename: Path = tmpdir / "test_vacancies.json"
    filename_str: str = str(filename)
    with open(filename_str, "w", encoding="utf-8") as f:
        json.dump([], f)

    vacancies: List[Vacancy] = load_vacancies_from_file(filename_str)
    assert len(vacancies) == 0
