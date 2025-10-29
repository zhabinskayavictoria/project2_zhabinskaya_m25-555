def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata
    columns = ['ID:int'] + columns
    for col in columns:
        name, dtype = col.split(':')
        if dtype not in ('int', 'str', 'bool'):
            print(f'Ошибка: Неверный тип данных для столбца {name}.')
            return metadata
    metadata[table_name] = {'columns': columns}
    print(f'Таблица "{table_name}" успешно создана со столбцами: {", ".join(columns)}')
    return metadata

def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata
    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata
