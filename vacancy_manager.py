from abc import ABC, abstractmethod
import json

class VacancyManager(ABC):
    """
    Этот класс объявляет абстрактные методы, которые позже
    будут переопределены в дочерних классах
    """
    @abstractmethod
    def add_vacancy(self, vacancy):
        """
        Этот абстрактный метод получает и перебирает вакансии
        """
        pass

    @abstractmethod
    def get_vacancies(self, criteria):
        """
        Этот абстрактный метод отбирает полученные вакансии по заданному критерию
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id):
        """
        Этот метод удаляет не подходящие по критерию вакансии
        """
        pass


class JSONVacancyManager(VacancyManager):
    def __init__(self, file_name):
        self.file_name = file_name

    def add_vacancy(self, vacancy):
        if not isinstance(vacancy, Vacancy):
            raise ValueError("Expected a Vacancy instance")
        try:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                vacancies = json.load(file)
        except FileNotFoundError:
            vacancies = []

        vacancies.append(vacancy.__dict__)
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)

    def get_vacancies(self, criteria):
        with open(self.file_name, 'r', encoding='utf-8') as file:
            vacancies = json.load(file)

        filtered_vacancies = [vac for vac in vacancies if all(vac.get(k) == v for k, v in criteria.items())]
        return filtered_vacancies

    def delete_vacancy(self, vacancy_id):
        with open(self.file_name, 'r', encoding='utf-8') as file:
            vacancies = json.load(file)

        vacancies = [vac for vac in vacancies if vac.get('id') != vacancy_id]
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)

