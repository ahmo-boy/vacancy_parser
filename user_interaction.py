from parser import HH
from vacancy_manager import JSONVacancyManager

def user_interaction():
    '''
    Функция - позволящая взаимодействовать с
    '''
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
