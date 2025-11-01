import shlex

import prompt
from prettytable import PrettyTable

from .constants import META_FILE
from .core import (
    create_table,
    delete,
    drop_table,
    insert,
    select,
    update,
)
from .parser import (
    parse_delete_command,
    parse_insert_command,
    parse_select_command,
    parse_update_command,
)
from .utils import load_metadata, load_table_data, save_metadata, save_table_data


def print_help():
    """Выводит справочную информацию по доступным командам."""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print('\n***Операции с данными***')
    print('Функции:')
    print('<command> insert into <имя_таблицы> values (<значение1>, '
        '<значение2>, ...) - создать запись.')
    print('<command> select from <имя_таблицы> where <столбец> '
        '= <значение> - прочитать записи по условию.')
    print('<command> select from <имя_таблицы> - прочитать все записи.')
    print('<command> update <имя_таблицы> set <столбец1> = <новое_значение1> '
        'where <столбец_условия> = <значение_условия> - обновить запись.')
    print('<command> delete from <имя_таблицы> where '
        '<столбец> = <значение> - удалить запись.')
    print('<command> info <имя_таблицы> - вывести информацию о таблице.')
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def run():
    """Главный цикл - обработка команд"""
    print_help()
    while True:
        metadata = load_metadata(META_FILE)
        user_input = prompt.string('Введите команду: ').strip()
        
        try:
            args = shlex.split(user_input)
        except ValueError:
            print("Ошибка парсинга команды. Попробуйте снова\n")
            continue   
        
        command = args[0].lower()
        if command == "create_table":
            if len(args) < 3:
                print("Недостаточно аргументов для create_table.\n")
                continue
            table_name = args[1]
            columns = args[2:]
            metadata = create_table(metadata, table_name, columns)
            save_metadata(META_FILE, metadata)
        
        elif command == "drop_table":
            if len(args) != 2:
                print("Неверное количество аргументов для drop_table.\n")
                continue
            table_name = args[1]
            metadata = drop_table(metadata, table_name)
            save_metadata(META_FILE, metadata)

        elif command == "list_tables":
            if metadata:
                for t in metadata.keys():
                    print(f"- {t}")
                print()
            else:
                print("Список таблиц пуст.\n")  
        
        elif command == 'insert':
            table_name, values = parse_insert_command(user_input)
            if table_name and values:
                data = insert(metadata, table_name, values)
                if data is not None:
                    save_table_data(table_name, data)

        elif command == 'select':
            table_name, where_clause = parse_select_command(user_input)
            if table_name:
                if table_name not in metadata:
                    print(f'Ошибка: таблица {table_name} не существует.\n')
                    continue
                table_data = load_table_data(table_name)
                result = select(table_data, where_clause)
                if result:
                    table_meta = metadata[table_name]
                    columns = [col.split(':')[0] for col in table_meta['columns']]
                    pt = PrettyTable()
                    pt.field_names = columns
                    for row in result:
                        pt.add_row([row.get(col, '') for col in columns])
                    print(pt)
                    print()
                else:
                    print("Записей не найдено.\n")

        elif command == 'update':
            table_name, set_clause, where_clause = parse_update_command(user_input)
            if table_name and set_clause and where_clause:
                if table_name not in metadata:
                    print(f'Ошибка: таблица {table_name} не существует.\n')
                    continue
                table_data = load_table_data(table_name)
                updated_data, updated_ids = update(table_data, set_clause, where_clause)
                if updated_ids:
                    save_table_data(table_name, updated_data)
                    for uid in updated_ids:
                        print(
                        f'Запись с ID={uid} в таблице "{table_name}" '
                        f'успешно обновлена.'
                    )
                    print()
                else:
                    print("Записей для обновления не найдено.\n")

        elif command == 'delete':
            table_name, where_clause = parse_delete_command(user_input)
            if table_name and where_clause:
                if table_name not in metadata:
                    print(f'Ошибка: таблица {table_name} не существует.\n')
                    continue
                table_data = load_table_data(table_name)
                new_data, deleted_ids = delete(table_data, where_clause)
                if deleted_ids:
                    save_table_data(table_name, new_data)
                    for did in deleted_ids:
                        print(
                            f'Запись с ID={did} успешно удаллена из таблицы '
                            f'"{table_name}".'
                        )
                    print()
                else:
                    print("Записей для удаления не найдено.\n")

        elif command == 'info':
            if len(args) != 2:
                print("Неверное количество аргументов для info.\n")
                continue
            table_name = args[1]
            if table_name not in metadata:
                print(f'Ошибка: таблица {table_name} не существует.\n')
                continue
            table_meta = metadata[table_name]
            columns = ", ".join(table_meta['columns'])
            table_data = load_table_data(table_name)
            count = len(table_data)
            print(f"Таблица: {table_name}")
            print(f"Столбцы: {columns}")
            print(f"Количество записей: {count}\n")

        elif command == 'exit':
            print('До свидания!')
            break
        
        elif command == 'help':
            print_help()
        
        else:
            print(f'Функции "{command}" нет. Попробуйте снова.\n')