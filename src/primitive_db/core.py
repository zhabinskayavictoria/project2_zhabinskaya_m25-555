from .constants import VALID_TYPES
from .decorators import confirm_action, handle_db_errors, log_time
from .utils import load_table_data


@handle_db_errors
@log_time
def select(table_data, where_clause=None):
    """Выбирает записи из table_data"""
    if where_clause is None:
        return table_data
    
    filtered_data = []
    filtered_data = [
    row for row in table_data
    if all(
        column in row and row[column] == value 
        for column, value in where_clause.items())
    ]
    return filtered_data


@handle_db_errors
def update(table_data, set_clause, where_clause):
    """Находит записи по where_clause, обновляет в 
    найденных записях поля согласно set_clause"""
    if not set_clause or not where_clause:
        print("Ошибка: не заданы условия для update.\n")
        return table_data, []
    
    updated_ids = []
    for row in table_data:
        if all(column in row and row[column] == value 
            for column, value in where_clause.items()):
            row.update({
                k: v for k, v in set_clause.items() 
                if k in row and k != 'ID'})
            if any(k in row and row[k] == v for k, v in set_clause.items()):
                updated_ids.append(row['ID'])
    return table_data, updated_ids


@handle_db_errors
@confirm_action("удаление записей")
def delete(table_data, where_clause):
    """Находит записи по where_clause и удаляет их"""
    if not where_clause:
        print("Ошибка: не заданы условия для delete.\n")
        return table_data, []
    
    deleted_ids = []
    new_data = []
    for row in table_data:
        match = True
        for column, value in where_clause.items():
            if column not in row or row[column] != value:
                match = False
                break
        if match:
            deleted_ids.append(row['ID'])
        else:
            new_data.append(row)
    return new_data, deleted_ids


@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    """Добавляет записи в таблицу"""
    if table_name not in metadata:
        print(f'Ошибка: таблица {table_name} не существует.\n')
        return None

    table_meta = metadata[table_name]
    columns = table_meta['columns']
    if len(values) != len(columns) - 1:
        print("Ошибка: неверное количество значений.\n")
        return None

    data = load_table_data(table_name)
    if data:
        new_id = max(row['ID'] for row in data) + 1
    else:
        new_id = 1

    new_record = {'ID': new_id}
    for col, val in zip(columns[1:], values):
        name, dtype = col.split(':')
        val = val.strip('"\'')  
        if dtype == 'int':
            val = int(val)
        elif dtype == 'bool':
            val = val.lower() in ('true', '1')
        elif dtype == 'str':
            val = val
        else:
            raise ValueError(f"Неподдерживаемый тип данных {dtype}")
        new_record[name] = val

    data.append(new_record)
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return data


@handle_db_errors
def create_table(metadata, table_name, columns):
    """Создает таблицу с проверками и добавлением 
    ID:int (гарантированно первый столбец)"""
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.\n')
        return metadata

    parsed_columns = []
    has_id = False
    for col in columns:
        if ':' not in col:
            print(f"Некорректное значение: {col}. Попробуйте снова.\n")
            return metadata
        name, dtype = col.split(':', 1)
        if dtype not in VALID_TYPES:
            print(f"Некорректное значение типа: {dtype}. Попробуйте снова.\n")
            return metadata
        parsed_columns.append(f"{name}:{dtype}")
        if name == "ID" and dtype == "int":
            has_id = True

    if not has_id:
        parsed_columns.insert(0, "ID:int")

    metadata[table_name] = {"columns": parsed_columns}
    print(
    f'Таблица "{table_name}" успешно создана со столбцами: '
    f'{", ".join(parsed_columns)}\n'
    )
    return metadata


@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    """Удаляет таблицу, если она существует"""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.\n')
        return metadata
    
    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.\n')
    return metadata


