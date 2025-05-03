from typing import Any, Dict, Optional
from unittest.mock import MagicMock, patch

import pytest
import requests

from src.api_client import HeadHunterAPI


# Тест для проверки создания User-Agent
def test_create_user_agent(hh_api: HeadHunterAPI) -> None:
    user_agent = hh_api._create_user_agent()
    assert isinstance(user_agent, str)
    assert "MyVacancyParser" in user_agent  # Проверяем, что название приложения указано


# Тест для проверки подключения к API (мокируем requests.get)
@patch("requests.get")
def test_connect_success(mock_get: MagicMock, hh_api: HeadHunterAPI) -> None:
    mock_get.return_value.raise_for_status = lambda: None  # Успешный статус код
    hh_api._connect()  # Проверяем, что не возникает исключений


# Тест для проверки подключения к API при ошибке (мокируем requests.get)
@patch("requests.get")
def test_connect_failure(mock_get: MagicMock, hh_api: HeadHunterAPI) -> None:
    mock_get.side_effect = requests.exceptions.RequestException("Connection error")
    with pytest.raises(ConnectionError):
        hh_api._connect()


# Тест для проверки получения вакансий (мокируем requests.get)
@patch("requests.get")
def test_get_vacancies_success(mock_get: MagicMock, hh_api: HeadHunterAPI) -> None:
    """Тест успешного получения вакансий."""
    # Мокируем успешный ответ API
    mock_response: Dict[str, Any] = {
        "items": [{"name": "Python Developer", "url": "url1"}, {"name": "Data Scientist", "url": "url2"}],
        "found": 2,
        "pages": 1,
        "per_page": 100,
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    vacancies: Optional[Dict[str, Any]] = hh_api.get_vacancies("Python", "113", page=0)
    if vacancies is not None:
        assert isinstance(vacancies["items"], list)  # Проверяем, что vacancies['items'] - это список
        assert len(vacancies["items"]) == 2  # Проверяем длину списка
        assert vacancies["items"][0]["name"] == "Python Developer"  # Проверяем элемент списка
    else:
        assert False, "Vacancies не должно быть None"


# Тест для проверки получения вакансий при ошибке API (мокируем requests.get)
@patch("requests.get")
def test_get_vacancies_failure(mock_get: MagicMock, hh_api: HeadHunterAPI) -> None:
    mock_get.side_effect = requests.exceptions.RequestException("API error")
    vacancies = hh_api.get_vacancies("Python", "113", page=0)
    assert vacancies is None


# Параметризованный тест для различных сценариев запроса вакансий (мокируем requests.get)
@pytest.mark.parametrize(
    "search_query, area, page, expected_count",
    [
        ("Python", "113", 0, 2),  # Успешный запрос
        ("Java", "1", 0, 0),  # Нет вакансий по запросу
    ],
)
@patch("requests.get")
def test_get_vacancies_parameterized(
    mock_get: MagicMock,
    hh_api: HeadHunterAPI,
    search_query: str,
    area: str,
    page: int,
    expected_count: int,
) -> None:
    """Параметризованный тест для get_vacancies."""
    # Мокируем ответ API в зависимости от параметров
    if search_query == "Python":
        mock_response: Dict[str, Any] = {
            "items": [{"name": "Python Developer", "url": "url1"}, {"name": "Data Scientist", "url": "url2"}],
            "found": 2,
            "pages": 1,
            "per_page": 100,
        }
    else:
        mock_response = {"items": [], "found": 0, "pages": 0, "per_page": 100}
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    vacancies: Optional[Dict[str, Any]] = hh_api.get_vacancies(search_query, area, page)
    if expected_count > 0:
        if vacancies is not None:
            assert isinstance(vacancies["items"], list)
            assert len(vacancies["items"]) == expected_count
        else:
            assert False, "Vacancies не должно быть None при expected_count > 0"
    else:
        assert vacancies is not None and vacancies["items"] == mock_response["items"]
