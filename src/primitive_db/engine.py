import prompt
import shlex
from .utils import load_metadata, save_metadata
from .core import create_table, drop_table
from .constants import META_FILE

def print_help():
    """Выводит справочную информацию по доступным командам."""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def run():
    print_help()
    while True:
        metadata = load_metadata(META_FILE)
        user_input = prompt.string('Введите команду: ').strip().lower()
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
            else:
                print("Список таблиц пуст.\n")  
                
        elif command == 'exit':
            print('До свидания!')
            break
        
        elif command == 'help':
            print_help()
        
        else:
            print(f'Команда "{command}" не распознана. Попробуйте снова.\n')




