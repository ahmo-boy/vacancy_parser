from abc import ABC, abstractmethod
import json

class VacancyManager(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, criteria):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id):
        pass


class JSONVacancyManager(VacancyManager):
    def __init__(self, file_name):
        self.file_name = file_name

    def add_vacancy(self, vacancy):
        try:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                vacancies = json.load(file)
        except FileNotFoundError:
            vacancies = []

        vacancies.append(vacancy)
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
