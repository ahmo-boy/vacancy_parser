from abc import ABC, abstractmethod
import json
import requests

class Parser(ABC):
    def __init__(self, file_worker):
        self.file_worker = file_worker
        self.vacancies = [] # инициализируем список ваканский в родительском классе

    @abstractmethod
    def load_vacancies(self, keyword):
        """
        Метод для загрузки ваканский.
        Должен быть реализован в дочернем классе.
        """
        pass

    @abstractmethod
    def parse_vacancy(self, vacancy):
        """
        Метод для парсинга вакансий.
        Должен быть реализован в дочернем классе.
        """
        pass

    def save_vacancies_to_file(self, filename):
        """
        Метод для сохранения вакансий в файл.
        """
        with open(filename, 'w', encoding='utf-8') as f:
            for vacancy in self.vacancies:
                f.write(f"{vacancy}\n")

    def load_vacancies_from_file(self, filename):
        """
        Метод для загрузки вакансий из файла.
        """
        with open(filename, 'r', encoding='utf-8') as f:
            self.vacancies = [line.strip() for line in f]


class VacancyManager(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        """
        Метод для добавления вакансии в файл.
        """
        pass

    @abstractmethod
    def get_vacancies(self, criteria):
        """
        Метод для получения данных из файла по указанным критериям.
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id):
        """
        Метод для удаления информации о вакансии.
        """
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


class HH(Parser):
    """
    Класс для работы с API HeadHunter
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
                vacancies = response.json()['items', []]
                if not vacancies:
                    break
                self.vacancies.extend(vacancies)
                self.params['page'] += 1
            else:
                print(f'Failed to get data: {response.status_code}')
                break

    def parse_vacancy(self, vacancy):
        """
        Пример метода для парсинга отдельной вакансии.
        """
        return {
            'id': vacancy['id'],
            'name': vacancy['name'],
            'employer': vacancy['employer']['name'],
            'salary': vacancy['salary'],
            'area': vacancy['area']
        }


def user_interaction():
    json_manager = JSONVacancyManager('vacancies.json')
    hh = HH(json_manager)

    while True:
        print("\n1. Ввести поисковый запрос для запроса вакансий из hh.ru")
        print("2. Получить топ N вакансий по зарплате")
        print("3. Получить вакансии с ключевым словом в описании")
        print("4. Сохранить вакансии в файл")
        print("5. Загрузить вакансии из файла")
        print("6. Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
            keyword = input("Введите поисковый запрос: ")
            hh.load_vacancies(keyword)
            print(f"Загружено {len(hh.vacancies)} вакансий.")

        elif choice == '2':
            N = int(input("Введите количество вакансий для отображения: "))
            top_vacancies = sorted(hh.vacancies, key=lambda x: x['salary'] if x['salary'] else 0, reverse=True)[:N]
            for vac in top_vacancies:
                print(hh.parse_vacancy(vac))

        elif choice == '3':
            keyword = input("Введите ключевое слово для поиска в описании: ")
            filtered_vacancies = [vac for vac in hh.vacancies if keyword.lower() in (vac['description'].lower() if vac.get('description') else '')]
            for vac in filtered_vacancies:
                print(hh.parse_vacancy(vac))

        elif choice == '4':
            filename = input("Введите имя файла для сохранения: ")
            hh.save_vacancies_to_file(filename)
            print(f"Вакансии сохранены в файл {filename}.")

        elif choice == '5':
            filename = input("Введите имя файла для загрузки: ")
            hh.load_vacancies_from_file(filename)
            print(f"Вакансии загружены из файла {filename}.")

        elif choice == '6':
            break

        else:
            print("Неверный ввод, попробуйте еще раз.")

if __name__ == "__main__":
    user_interaction()