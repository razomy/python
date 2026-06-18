import functools
import time
import inspect


def universal_log(message):
    def inner(func):
        # 1. Если это АСИНХРОННЫЙ ГЕНЕРАТОР (async def с yield)
        if inspect.isasyncgenfunction(func):
            @functools.wraps(func)
            async def async_gen_wrapper(*args, **kwargs):
                start = time.perf_counter()
                print(f"⏳ [Async Gen] {message} Start...")

                first_item_received = False
                async for item in func(*args, **kwargs):
                    if not first_item_received:
                        ttft = time.perf_counter() - start
                        print(f"🚀 [Async Gen] {message} First response received in {ttft:.6f}s")
                        first_item_received = True
                    yield item

                end = time.perf_counter()
                print(f"✅ [Async Gen] {message} Finish! Total time: {end - start:.6f}s")

            return async_gen_wrapper

            # 2. Если это ОБЫЧНАЯ АСИНХРОННАЯ ФУНКЦИЯ (async def)
        elif inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                start = time.perf_counter()
                print(f"⏳ [Async] {message} Start...")
                result = await func(*args, **kwargs)
                end = time.perf_counter()
                print(f"✅ [Async] {message} Finish! {end - start:.6f}s")
                return result

            return async_wrapper

            # 3. Если это СИНХРОННАЯ ФУНКЦИЯ ИЛИ СИНХРОННЫЙ ГЕНЕРАТОР
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                start = time.perf_counter()
                print(f"⏳ [Sync] {message} Start...")
                result = func(*args, **kwargs)

                # Проверяем динамически: если функция вернула генератор
                if inspect.isgenerator(result):
                    def gen_wrapper():
                        first_item_received = False
                        # Используем yield from, но чтобы вклиниться в первый элемент,
                        # итерируемся вручную через цикл
                        for item in result:
                            if not first_item_received:
                                ttft = time.perf_counter() - start
                                print(f"🚀 [Sync Gen] {message} First response received in {ttft:.6f}s")
                                first_item_received = True
                            yield item

                        end = time.perf_counter()
                        print(f"✅ [Sync Gen] {message} Finish! Total time: {end - start:.6f}s")

                    return gen_wrapper()

                    # Если это просто обычная функция
                end = time.perf_counter()
                print(f"✅ [Sync] {message} Finish! {end - start:.6f}s")
                return result

            return sync_wrapper

    return inner


