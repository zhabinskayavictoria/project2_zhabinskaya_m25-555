import time

def handle_db_errors(func):
    """Декоратор для обработки ошибок БД"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден. Возможно, база данных не инициализирована.")
            return None
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
            return None
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
            return None
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
            return None
    wrapper.__name__ = func.__name__
    return wrapper

def confirm_action(action_name):
    """
    Фабрика декораторов для запроса подтверждения операции.
    Отменяет, если ввод не 'y'
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            prompt = f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            resp = input(prompt).strip().lower()
            if resp != 'y':
                print("Операция отменена.")
                return None
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator

def log_time(func):
    """Декоратор для замера времени выполнения функции"""
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        end = time.monotonic()
        elapsed = end - start
        print(f"Функция {func.__name__} выполнилась за {elapsed:.3f} секунд.")
        return result
    wrapper.__name__ = func.__name__
    return wrapper
