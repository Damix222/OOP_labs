from src.lib.model import Product
from src.lib.normalize import normalize


class ProductCatalog:
    def __init__(self):
        self._items = []

    def add(self, item):
        if not isinstance(item, Product):
            raise TypeError('В каталог можно добавлять только объекты Product')

        new_name = normalize(item.name)

        for product in self._items:
            if normalize(product.name) == new_name:
                raise ValueError(f"Товар с названием '{item.name}' уже есть в каталоге")

        self._items.append(item)

    def remove(self, item):
        if not isinstance(item, Product):
            raise TypeError('Удалять можно только объект Product')

        if item not in self._items:
            raise ValueError('Такого товара нет в каталоге')

        self._items.remove(item)

    def remove_at(self, index):
        if not isinstance(index, int):
            raise TypeError('Индекс должен быть целым числом')

        if index < 0 or index >= len(self._items):
            raise IndexError('Индекс вне диапазона')

        del self._items[index]

    def get_all(self):
        return self._items.copy()

    def find_by_name(self, name):
        search_name = normalize(name)

        for item in self._items:
            if normalize(item.name) == search_name:
                return item

        return None

    def find_by_category(self, category):
        search_category = normalize(category)
        result = ProductCatalog()

        for item in self._items:
            if normalize(item.category) == search_category:
                result.add(item)

        return result

    def sort_by_name(self, reverse=False):
        sorted_catalog = ProductCatalog()
        sorted_items = sorted(
            self._items,
            key=lambda item: normalize(item.name),
            reverse=reverse
        )

        for item in sorted_items:
            sorted_catalog.add(item)

        return sorted_catalog

    def sort_by_price(self, reverse=False):
        sorted_catalog = ProductCatalog()
        sorted_items = sorted(
            self._items,
            key=lambda item: item.price,
            reverse=reverse
        )

        for item in sorted_items:
            sorted_catalog.add(item)

        return sorted_catalog

    def get_active(self):
        result = ProductCatalog()

        for item in self._items:
            if item.is_active:
                result.add(item)

        return result

    def get_available(self):
        result = ProductCatalog()

        for item in self._items:
            if item.stock > 0:
                result.add(item)

        return result

    def get_expensive(self, min_price):
        if isinstance(min_price, bool) or not isinstance(min_price, (int, float)):
            raise TypeError('Минимальная цена должна быть числом')

        result = ProductCatalog()

        for item in self._items:
            if item.price >= min_price:
                result.add(item)

        return result

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index):
        return self._items[index]

    def __str__(self):
        if not self._items:
            return 'Каталог пуст'

        lines = []
        for i, item in enumerate(self._items, start=1):
            lines.append(
                f'{i}. {item.name} | {item.category} | '
                f'Цена: {item.price:.2f} | Остаток: {item.stock} | '
                f'Активен: {item.is_active}'
            )

        return '\n'.join(lines)