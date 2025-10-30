from .constants import VALID_TYPES

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


