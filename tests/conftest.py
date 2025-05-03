import os
from pathlib import Path
from typing import Any, Dict, Generator
from unittest.mock import MagicMock, patch

import pytest

from src.api_client import HeadHunterAPI
from src.file_manager import CSVFileManager, JSONFileManager
from src.vacancy import Vacancy


@pytest.fixture
def hh_api() -> HeadHunterAPI:
    return HeadHunterAPI()


@pytest.fixture
def json_file_manager(tmpdir: Path) -> Generator[JSONFileManager, None, None]:
    """Фикстура для создания временного JSONFileManager."""
    filename = tmpdir / "test_vacancies.json"
    file_manager = JSONFileManager(str(filename))
    yield file_manager
    if os.path.exists(str(filename)):
        os.remove(str(filename))


@pytest.fixture
def csv_file_manager(tmpdir: Path) -> Generator[CSVFileManager, None, None]:
    """Фикстура для создания временного CSVFileManager."""
    filename = tmpdir / "test_vacancies.csv"
    file_manager = CSVFileManager(str(filename))
    yield file_manager
    if os.path.exists(str(filename)):
        os.remove(str(filename))


@pytest.fixture
def mock_hh_api() -> Generator[MagicMock, None, None]:
    """Фикстура для мокирования HeadHunterAPI."""
    with patch("src.utils.HeadHunterAPI") as MockHeadHunterAPI:
        mock_api = MockHeadHunterAPI.return_value
        yield mock_api


@pytest.fixture
def sample_hh_item() -> Dict[str, Any]:
    """Фикстура для создания sample_hh_item."""
    return {
        "name": "Python Developer",
        "alternate_url": "https://example.com/vacancy/123",
        "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
        "snippet": {"requirement": "Python, Django", "responsibility": "Develop web applications"},
    }


@pytest.fixture
def sample_vacancy() -> Vacancy:
    """Фикстура для создания sample_vacancy."""
    return Vacancy(
        title="Python Developer",
        url="https://example.com/vacancy/123",
        salary_from=100000,
        salary_to=150000,
        description="Python, Django Develop web applications",
    )
