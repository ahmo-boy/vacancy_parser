from abc import ABC, abstractmethod
import requests

class Parser(ABC):
    def __init__(self, file_worker):
        self.file_worker = file_worker
        self.vacancies = []

    @abstractmethod
    def load_vacancies(self, keyword):
        pass

    @abstractmethod
    def parse_vacancy(self, vacancy):
        pass

    def save_vacancies_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            for vacancy in self.vacancies:
                f.write(f"{vacancy}\n")

    def load_vacancies_from_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            self.vacancies = [line.strip() for line in f]


class HH(Parser):
    def __init__(self, file_worker):
        super().__init__(file_worker)
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}

    def load_vacancies(self, keyword):
        self.params['text'] = keyword
        while self.params['page'] < 20:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            if response.status_code == 200:
                vacancies = response.json()['items', []]
                if not vacancies:
                    break
                self.vacancies.extend(vacancies)
                self.params['page'] += 1
            else:
                print(f'Failed to get data: {response.status_code}')
                break

    def parse_vacancy(self, vacancy):
        return {
            'id': vacancy['id'],
            'name': vacancy['name'],
            'employer': vacancy['employer']['name'],
            'salary': vacancy['salary'],
            'area': vacancy['area']
        }
