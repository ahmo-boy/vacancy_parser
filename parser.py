from abc import ABC, abstractmethod
import requests


class Parser(ABC):
    """
    Класс Parser - загужает, перибирает вакансии. А также сохраняет и выводит из файла
    """
    def __init__(self, file_worker):
        """
        Метод - инициатор
        """
        self.file_worker = file_worker
        self.vacancies = []

    @abstractmethod
    def load_vacancies(self, keyword):
        '''
        Метод загружающий вакансии, позже перезапишется в дочернем классе
        '''
        pass

    @abstractmethod
    def parse_vacancy(self, vacancy):
        '''
        Метод перебирающий вакансии по критериям, позже перезапишется в дочернем классе
        '''
        pass

    def save_vacancies_to_file(self, filename):
        '''
        Метод сохраняющий отобранные вакансии в файл
        '''
        with open(filename, 'a', encoding='utf-8') as f:
            for vacancy in self.vacancies:
                f.write(f"{vacancy}\n")

    def load_vacancies_from_file(self, filename):
        '''
        Метод получающий вакансии из файла
        '''
        with open(filename, 'r', encoding='utf-8') as f:
            self.vacancies = [line.strip() for line in f]


class HH(Parser):
    """
    Этот класс дочерний от класса Parser, он переопределяет родительские методы, позволяя загрузить
    """
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
                vacancies = response.json()['items']
                if not vacancies:
                    break
                self.vacancies.extend([Vacancy(vac) for vac in vacancies])
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


class Vacancy:
    def __init__(self, vacancy):
        # Используем метод parse_vacancy для извлечения информации о вакансии
        self.id = vacancy['id']
        self.name = vacancy['name']
        self.employer = vacancy['employer']['name']
        self.salary = self.validate_salary(vacancy['salary'])
        self.area = vacancy['area']['name']

    def validate_salary(self, salary): # проверяет значение зарплаты, так мы не получим ошибку если зарплата не указана
        if salary is None:
            print("Warning: Salary is not specified. Setting salary to 0.")
            return 0
        elif isinstance(salary, (int, float)) and salary >= 0:
            return salary
        else:
            raise ValueError("Invalid salary value")

    def __lt__(self, other):
        return self.salary < other.salary

    def __eq__(self, other):
        return self.salary == other.salary
