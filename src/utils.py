from typing import Dict, List, Optional

from src.api_client import HeadHunterAPI
from src.file_manager import JSONFileManager
from src.vacancy import Vacancy


def get_vacancies_from_hh(search_query: str, area_id: str, num_pages: int = 1) -> List[Vacancy]:
    """Получает вакансии с hh.ru и возвращает список объектов Vacancy."""
    hh_api = HeadHunterAPI()
    vacancies: List[Vacancy] = []
    for page in range(num_pages):
        data = hh_api.get_vacancies(search_query, area_id, page)
        if not data or "items" not in data:
            continue
        for item in data["items"]:
            vacancy = create_vacancy_from_hh_item(item)
            if vacancy:
                vacancies.append(vacancy)
    return vacancies


def create_vacancy_from_hh_item(item: Dict) -> Optional[Vacancy]:
    """Создает объект Vacancy из элемента, полученного от API hh.ru."""
    try:
        salary_from = item["salary"]["from"] if item["salary"] and item["salary"]["from"] else 0
        salary_to = item["salary"]["to"] if item["salary"] and item["salary"]["to"] else 0
    except (TypeError, KeyError):
        salary_from = 0
        salary_to = 0

    try:
        description = item["snippet"]["requirement"] or item["snippet"]["responsibility"] or ""
    except (TypeError, KeyError):
        description = ""

    try:
        vacancy = Vacancy(
            title=item["name"],
            url=item["alternate_url"],
            salary_from=salary_from,
            salary_to=salary_to,
            description=description,
        )
        return vacancy
    except KeyError:
        return None


def display_vacancies(vacancies: List[Vacancy]) -> None:
    """Выводит информацию о вакансиях в консоль в удобочитаемом формате."""
    if not vacancies:
        print("Нет вакансий для отображения.")
        return

    for vacancy in vacancies:
        print(f"Название: {vacancy.title}")
        print(f"Ссылка: {vacancy.url}")
        print(f"Зарплата: {vacancy.salary_from} - {vacancy.salary_to}")
        print(f"Описание: {vacancy.description}")
        print("-" * 20)


def save_vacancies_to_file(vacancies: List[Vacancy], filename: str) -> None:
    """Сохраняет список вакансий в JSON-файл."""
    file_manager = JSONFileManager(filename)
    for vacancy in vacancies:
        file_manager.add_vacancy(dict(vacancy))
    print(f"Сохранено {len(vacancies)} вакансий в {filename}")


def load_vacancies_from_file(filename: str) -> List[Vacancy]:
    """Загружает список вакансий из JSON-файла и преобразует его в объекты Vacancy."""
    file_manager = JSONFileManager(filename)
    vacancy_data = file_manager.get_vacancies()
    vacancies = []
    for data in vacancy_data:
        vacancy = Vacancy(**data)  # Создаем Vacancy объект из словаря
        vacancies.append(vacancy)
    return vacancies


def interact_with_user() -> None:
    """Функция для взаимодействия с пользователем через консоль.
    Организует поиск, фильтрацию и отображение вакансий."""
    search_query = input("Введите поисковый запрос: ")
    area_id = input("Введите ID города (оставьте пустым для поиска по России): ")
    if not area_id:
        area_id = "113"
    num_pages = int(input("Сколько страниц поискать? "))
    vacancies = get_vacancies_from_hh(search_query, area_id, num_pages)

    if not vacancies:
        print("Нет вакансий, соответствующих запросу.")
        return

    filename = "data/vacancies.json"
    save_vacancies_to_file(vacancies, filename)

    try:
        n = int(input("Введите количество топ вакансий по зарплате, которые хотите увидеть: "))
        top_vacancies = sorted(vacancies, reverse=True)[:n]
        print("\nТоп вакансии по зарплате:")
        display_vacancies(top_vacancies)
    except ValueError:
        print("Некорректный ввод для количества вакансий.")

    keyword = input("Введите ключевое слово для поиска в описании: ")
    keyword_vacancies = [
        vacancy for vacancy in vacancies if vacancy.description and keyword.lower() in vacancy.description.lower()
    ]
    print(f"\nВакансии с ключевым словом '{keyword}':")
    display_vacancies(keyword_vacancies)
