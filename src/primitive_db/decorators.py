import time


def handle_db_errors(func):
    """Декоратор для обработки ошибок БД"""
    def wrapper(*args, **kwargs):
        """
        Обёртка для функции с обработкой исключений
        Возвращает: результат func() или None при ошибке
        """
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print('Ошибка: Файл данных не найден. Возможно, '
                'база данных не инициализирована.\n')
            return None
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.\n")
            return None
        except ValueError as e:
            print(f"Ошибка валидации: {e}\n")
            return None
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}\n")
            return None
    wrapper.__name__ = func.__name__
    return wrapper


def confirm_action(action_name):
    """
    Фабрика декораторов для запроса подтверждения операции
    Отменяет, если ввод не 'y'
    """
    def decorator(func):
        """
        Декоратор с запросом подтверждения.
        Возвращает: результат func() или None при отмене
        """
        def wrapper(*args, **kwargs):
            """
            Обёртка с вводом подтверждения
            Возвращает: результат func() или None
            """
            prompt = f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            resp = input(prompt).strip().lower()
            if resp != 'y':
                print("Операция отменена.\n")
                return None
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator


def log_time(func):
    """Декоратор для замера времени выполнения функции"""
    def wrapper(*args, **kwargs):
        """
        Обёртка с замером времени
        Возвращает: результат func()
        """
        start = time.monotonic()
        result = func(*args, **kwargs)
        end = time.monotonic()
        elapsed = end - start
        print(f"Функция {func.__name__} выполнилась за {elapsed:.3f} секунд.\n")
        return result
    wrapper.__name__ = func.__name__
    return wrapper


def create_cacher():
    """Создает замыкание с кэшем (словарь)"""
    cache = {}
    def cache_result(key, value_func):
        """
        Проверяет наличие результата в кэше.
        Если есть - возвращает, если нет - вычисляет и сохраняет.
        """
        if key in cache:
            print(f"Результат найден в кэше для ключа: {key}")
            return cache[key]
        value = value_func()
        cache[key] = value
        return value
    
    def clear_cache():
        cache.clear()

    cache_result.clear_cache = clear_cache
    return cache_result