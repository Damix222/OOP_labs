from src.lab02.collections import ProductCatalog as BaseProductCatalog


class ProductCatalog(BaseProductCatalog):
    """
    Расширенная коллекция товаров для ЛР-5.

    Добавляет поддержку функций-стратегий:
    - sort_by(key_func)
    - filter_by(predicate)
    - apply(func)
    """

    def _create_from_items(self, items):
        result = ProductCatalog()

        for item in items:
            result.add(item)

        return result

    def sort_by(self, key_func, reverse=False):
        """
        Сортирует коллекцию по переданной функции-стратегии.

        key_func — функция, которая принимает объект товара
        и возвращает ключ сортировки.
        """
        if not callable(key_func):
            raise TypeError('key_func должен быть вызываемым объектом')

        sorted_items = sorted(
            self,
            key=key_func,
            reverse=reverse
        )

        return self._create_from_items(sorted_items)

    def filter_by(self, predicate):
        """
        Фильтрует коллекцию по переданной функции-предикату.

        predicate — функция, которая принимает объект товара
        и возвращает True или False.
        """
        if not callable(predicate):
            raise TypeError('predicate должен быть вызываемым объектом')

        filtered_items = filter(predicate, self)

        return self._create_from_items(filtered_items)

    def apply(self, func):
        """
        Применяет произвольную функцию ко всем элементам коллекции.

        Возвращает список результатов.
        """
        if not callable(func):
            raise TypeError('func должен быть вызываемым объектом')

        return list(map(func, self))