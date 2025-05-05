from typing import Any, Iterator, Tuple


class Vacancy:
    """Класс для представления вакансии."""

    __slots__ = ("title", "url", "salary_from", "salary_to", "description")

    def __init__(self, title: str, url: str, salary_from: int = 0, salary_to: int = 0, description: str = ""):
        """Инициализация объекта Vacancy."""
        self.title = title
        self.url = url
        self.salary_from = self._validate_salary(salary_from)
        self.salary_to = self._validate_salary(salary_to)
        self.description = description

    def __gt__(self, other: object) -> bool:
        """Сравнение вакансий по зарплате (больше)."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_from > other.salary_from

    def __lt__(self, other: object) -> bool:
        """Сравнение вакансий по зарплате (меньше)."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_from < other.salary_from

    def __eq__(self, other: object) -> bool:
        """Сравнение вакансий по зарплате (равно)."""
        if not isinstance(other, Vacancy):
            return False
        return self.salary_from == other.salary_from

    def __str__(self) -> str:
        return f"{self.title} - {self.salary_from}-{self.salary_to} - {self.url}"

    def _validate_salary(self, salary: int) -> int:
        """Приватный метод для валидации зарплаты."""
        if not isinstance(salary, (int, float)):
            return 0
        return int(salary)

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Переопределяем метод __iter__ для преобразования объекта в словарь."""
        yield "title", self.title
        yield "url", self.url
        yield "salary_from", self.salary_from
        yield "salary_to", self.salary_to
        yield "description", self.description
