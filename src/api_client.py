import abc
from typing import Any, Dict, Optional

import requests


class APIClient(abc.ABC):
    """
    Абстрактный класс для работы с API сервисов с вакансиями.
    """

    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def _connect(self) -> None:
        """
        Абстрактный метод для подключения к API.
        """
        pass

    @abc.abstractmethod
    def get_vacancies(self, search_query: str, area: str, page: int = 0) -> Optional[Dict]:
        """
        Абстрактный метод для получения вакансий по заданному запросу.

        Args:
            search_query: поисковый запрос.
            page: номер страницы (для пагинации).

        Returns:
            Список вакансий.
        """
        pass


class HeadHunterAPI(APIClient):
    """
    Класс для работы с API hh.ru.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__base_url = "https://api.hh.ru"
        self.__headers = {"User-Agent": self._create_user_agent()}

    def _create_user_agent(self) -> str:
        """Создает User-Agent строку."""
        import platform

        import requests

        os_name = platform.system()
        os_version = platform.version()
        architecture = platform.machine()
        python_version = platform.python_version()
        requests_version = requests.__version__

        app_name = "MyVacancyParser"  # Замените на название вашего приложения
        version = "1.0"  # Замените на версию вашего приложения

        user_agent = (
            f"{app_name}/{version} ({os_name} {os_version}; "
            f"{architecture}) Python/{python_version} Requests/{requests_version}"
        )
        return user_agent

    def _connect(self) -> None:
        """
        Приватный метод для проверки подключения к API hh.ru.
        """
        try:
            response = requests.get(self.__base_url, headers=self.__headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Ошибка подключения к API hh.ru: {e}")

    def get_vacancies(self, search_query: str, area: str, page: int = 0) -> Optional[Dict[str, Any]]:
        """
        Получает список вакансий с hh.ru по заданному запросу.
        """
        url = f"{self.__base_url}/vacancies"
        params = {
            "text": search_query,
            "area": area,
            "page": page,
            "per_page": 100,  # Максимальное количество вакансий на странице
        }
        try:
            response = requests.get(url, params=params, headers=self.__headers)  # type: ignore
            response.raise_for_status()
            data: Dict[str, Any] = response.json()
            if "items" not in data:
                print("Ключ 'items' не найден в ответе API.")  # Выводим сообщение об ошибке
                return data  # Возвращаем  data
            return data
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении вакансий от hh.ru: {e}")
            return None


class MockHeadHunterAPI:
    def get_vacancies(self) -> Dict[str, Any]:
        """Мок для HeadHunterAPI."""
        return {"items": []}
