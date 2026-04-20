import importlib

module_cache = {}
def run_function_instant(package_name, function_name, args=None):
    args = args or []

    # Импортируем модуль
    if package_name in module_cache:
        module = module_cache[package_name]
    else:
        # Import and store in cache
        module = importlib.import_module(package_name)
        module_cache[package_name] = module

    # Проверяем, есть ли такая функция в модуле
    if not hasattr(module, function_name):
        raise AttributeError(f"Функция {function_name} не найдена в модуле {package_name}")

    # Получаем функцию
    func = getattr(module, function_name)

    # Вызываем: *args распаковывает список, **kwargs распаковывает словарь
    return func(*args)

