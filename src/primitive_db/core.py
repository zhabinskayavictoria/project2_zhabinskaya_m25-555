from .constants import VALID_TYPES
from prettytable import PrettyTable 

def insert(metadata, table_name, values):
    if table_name not in metadata:
        print(f'Ошибка: таблица {table_name} не существует.')
        return None

    table_meta = metadata[table_name]
    columns = table_meta['columns']

    if len(values) != len(columns) - 1:
        print("Ошибка: неверное количество значений.")
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
            val = str(val)
        new_record[name] = val

    data.append(new_record)
    save_table_data(table_name, data)
    return data

def select(table_data, where_clause=None):
    if not where_clause:
        return table_data
    result = []
    for row in table_data:
        if all(row.get(k) == v for k, v in where_clause.items()):
            result.append(row)
    return result

def update(table_data, set_clause, where_clause):
    count = 0
    for row in table_data:
        if all(row.get(k) == v for k, v in where_clause.items()):
            for k, v in set_clause.items():
                row[k] = v
            count += 1
    return table_data

def delete(table_data, where_clause):
    new_data = [row for row in table_data if not all(row.get(k) == v for k, v in where_clause.items())]
    return new_data


def create_table(metadata, table_name, columns):
    """Создает таблицу с проверками и добавлением ID:int (гарантированно первый столбец)."""
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
    print(f'Таблица "{table_name}" успешно создана со столбцами: {", ".join(parsed_columns)}\n')
    return metadata


def drop_table(metadata, table_name):
    """Удаляет таблицу, если она существует"""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.\n')
        return metadata
    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.\n')
    return metadata


