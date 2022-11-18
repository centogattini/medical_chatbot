import pandas as pd
from doctors_database import Database
if __name__ == '__main__':
    command = input('Здравствуйте!\nЕсли вы хотите посмотреть расписание специалиста, напишите "1"\nЕсли вы хотите обновить расписание, напишите "2"\n')
    print('-----------------------')
    if command == '1':
        db = Database('data\database.db')
        names = db.get_all_names()
        names_str = ''
        for i, name in enumerate(names):
            names_str += f'{i+1}. {name}\n'
        print(names_str)
        while True:
            command = input('Выберете врача из списка (в качестве ответа, введите его номер)\n')
            if int(command) in range(1,len(names)+1):
                break
            else:
                print('Вы ввели неверный номер врача. Повторите.')
        chosen_name = names[int(command)-1]
        columns, res = db.get_timetable_by_name(chosen_name)

        table = pd.DataFrame(res, columns=columns)
        from datetime import date
        table.to_csv(f'data/inner_usage_out/timetable_{date.today()}.csv')
        print(f'Таблица составлена. Вы можете найти ее в папке data/inner_usage_out.\nНазвание файла: inner_usage_out/timetable_{date.today()}.csv')
        print('До свидания!')
    else:
        print('Not implemented :(')

