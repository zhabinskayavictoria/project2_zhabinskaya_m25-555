import shlex


def parse_conditions(condition_str):
    """Разбирает строку условий вида "column = value" и возвращает словарь"""
    if not condition_str or condition_str.strip() == '':
        return None

    parts = condition_str.split('=', 1)
    if len(parts) != 2:
        print(f"Ошибка: некорректное условие '{condition_str}'\n")
        breakpoint
        return None
    
    column = parts[0].strip()
    value_str = parts[1].strip()
    if (
        value_str.startswith('"') and value_str.endswith('"')
    ) or (
        value_str.startswith("'") and value_str.endswith("'")
    ):
        value = value_str[1:-1]
    elif value_str.lower() in ('true', 'false'):
        value = value_str.lower() == 'true'
    else:
        try:
            value = int(value_str)
        except ValueError:
            value = value_str      
    return {column: value}


def parse_select_command(command_str):
    """Разбирает команду select и возвращает (table_name, where_clause) 
    или (None, None)"""
    try:
        command_lower = command_str.lower()
        if not command_lower.startswith('select from'):
            print("Ошибка: команда должна начинаться с 'select from'\n")
            return None, None
        
        rest = command_str[len('select from'):].strip()
        if 'where' in rest.lower():
            where_pos = rest.lower().index('where')
            table_name = rest[:where_pos].strip()
            condition_str = rest[where_pos + 5:].strip()
            where_clause = parse_conditions(condition_str)
        else:
            table_name = rest.strip()
            where_clause = None
        return table_name, where_clause
    except Exception as e:
        print(f"Ошибка парсинга команды select: {e}\n")
        return None, None


def parse_update_command(command_str):
    """Разбирает команду update и возвращает 
    (table_name, set_clause, where_clause) или (None, None, None)"""
    try:
        command_lower = command_str.lower()
        if not command_lower.startswith('update'):
            print("Ошибка: команда должна начинаться с 'update'\n")
            return None, None, None
        
        rest = command_str[len('update'):].strip()
        if 'set' not in rest.lower():
            print("Ошибка: отсутствует ключевое слово 'set'\n")
            return None, None, None
        
        set_pos = rest.lower().index('set')
        table_name = rest[:set_pos].strip()

        if 'where' not in rest.lower():
            print("Ошибка: отсутствует ключевое слово 'where'\n")
            return None, None, None
        
        where_pos = rest.lower().index('where')
        set_str = rest[set_pos + 3:where_pos].strip()
        where_str = rest[where_pos + 5:].strip()
        set_clause = parse_conditions(set_str)
        where_clause = parse_conditions(where_str)
        return table_name, set_clause, where_clause
    except Exception as e:
        print(f"Ошибка парсинга команды update: {e}\n")
        return None, None, None


def parse_delete_command(command_str):
    """Разбирает команду delete и возвращает (table_name, where_clause) 
    или (None, None)"""
    try:
        command_lower = command_str.lower()
        if not command_lower.startswith('delete from'):
            print("Ошибка: команда должна начинаться с 'delete from'\n")
            return None, None
        
        rest = command_str[len('delete from'):].strip()
        if 'where' not in rest.lower():
            print("Ошибка: отсутствует ключевое слово 'where'\n")
            return None, None
        
        where_pos = rest.lower().index('where')
        table_name = rest[:where_pos].strip()
        where_str = rest[where_pos + 5:].strip()
        where_clause = parse_conditions(where_str)
        return table_name, where_clause
    except Exception as e:
        print(f"Ошибка парсинга команды delete: {e}\n")
        return None, None


def parse_insert_command(command_str):
    """Разбирает строку insert и возвращает (table_name, values) или (None, None)"""
    try:
        tokens = shlex.split(command_str)
    except ValueError:
        print("Ошибка парсинга команды insert.\n")
        return None, None
    if len(tokens) < 5:
        print("Ошибка: слишком мало аргументов для insert.\n")
        return None, None
    if tokens[0].lower() != 'insert' or tokens[1].lower() != 'into':
        print("Ошибка: отсутствует ключевое слово 'insert into'.\n")
        return None, None
    if 'values' not in (t.lower() for t in tokens):
        print("Ошибка: отсутствует ключевое слово 'values'.\n")
        return None, None

    table_name = tokens[2]
    pos_values = command_str.lower().index('values') + len('values')
    values_str = command_str[pos_values:].strip()
    if not (values_str.startswith('(') and values_str.endswith(')')):
        print("Ошибка: значения должны быть в круглых скобках.\n")
        return None, None

    values_content = values_str[1:-1].strip()
    values = []
    current = ''
    inside_quotes = False
    quote_char = ''
    for ch in values_content:
        if ch in ('"', "'"):
            if not inside_quotes:
                inside_quotes = True
                quote_char = ch
                current += ch
            elif ch == quote_char:
                inside_quotes = False
                current += ch
            else:
                current += ch
        elif ch == ',' and not inside_quotes:
            values.append(current.strip())
            current = ''
        else:
            current += ch
    if current:
        values.append(current.strip())

    return table_name, values