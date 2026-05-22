from __future__ import annotations

from datetime import datetime
from pathlib import Path

from src.lab03.base import Product
from src.lab04.models import Accessory, DigitalProduct, Service
from src.lab06.container import TypedCollection
from src.lab07.exceptions import DuplicateItemError, ItemNotFoundError, StorageError
from src.lab07.storage import ProductItem, load, save
from src.lib.normalize import normalize


class ShopApp:
    """Бизнес-логика консольного приложения магазина."""

    def __init__(self, filepath: str | None = None) -> None:
        """Создать приложение и подготовить коллекцию товаров."""
        default_path = Path('data') / 'lab07_products.json'
        self._filepath = filepath or str(default_path)

        self._collection: TypedCollection[ProductItem] = TypedCollection(
            (Product, DigitalProduct, Service, Accessory)
        )
        self._added_at: dict[str, str] = {}

    def load_data(self) -> None:
        """Загрузить товары из JSON-файла в коллекцию."""
        try:
            items, added_at = load(self._filepath)
        except (OSError, ValueError, TypeError, KeyError) as error:
            raise StorageError(f'Не удалось загрузить данные: {error}') from error

        self._collection = TypedCollection((Product, DigitalProduct, Service, Accessory))
        self._added_at = added_at

        for item in items:
            try:
                self._collection.add(item)
            except ValueError as error:
                raise DuplicateItemError(str(error)) from error

            if item.name not in self._added_at:
                self._added_at[item.name] = self._now()

    def save_data(self) -> None:
        """Сохранить товары из коллекции в JSON-файл."""
        try:
            save(self._collection.get_all(), self._filepath, self._added_at)
        except OSError as error:
            raise StorageError(f'Не удалось сохранить данные: {error}') from error

    def add_product(
        self,
        name: str,
        price: float,
        stock: int,
        category: str,
        discount: float,
    ) -> None:
        """Добавить обычный товар."""
        product = Product(
            name=name,
            price=price,
            stock=stock,
            category=category,
            discount=discount,
        )

        self._add_item(product)

    def add_digital_product(
        self,
        name: str,
        price: float,
        stock: int,
        category: str,
        discount: float,
        file_size_mb: float,
        license_type: str,
    ) -> None:
        """Добавить цифровой товар."""
        product = DigitalProduct(
            name=name,
            price=price,
            stock=stock,
            category=category,
            discount=discount,
            file_size_mb=file_size_mb,
            license_type=license_type,
        )

        self._add_item(product)

    def add_service(
        self,
        name: str,
        price: float,
        stock: int,
        category: str,
        discount: float,
        duration_hours: float,
        on_site: bool,
    ) -> None:
        """Добавить услугу."""
        service = Service(
            name=name,
            price=price,
            stock=stock,
            category=category,
            discount=discount,
            duration_hours=duration_hours,
            on_site=on_site,
        )

        self._add_item(service)

    def add_accessory(
        self,
        name: str,
        price: float,
        stock: int,
        category: str,
        discount: float,
        compatibility: str,
        wireless: bool,
    ) -> None:
        """Добавить аксессуар."""
        accessory = Accessory(
            name=name,
            price=price,
            stock=stock,
            category=category,
            discount=discount,
            compatibility=compatibility,
            wireless=wireless,
        )

        self._add_item(accessory)

    def get_all_items(self) -> list[ProductItem]:
        """Вернуть все товары."""
        return self._collection.get_all()

    def find_by_name(self, name: str) -> ProductItem:
        """Найти товар по названию."""
        item = self._collection.find_by_name(name)

        if item is None:
            raise ItemNotFoundError(f"Товар '{name}' не найден")

        return item

    def filter_available(self) -> list[ProductItem]:
        """Вернуть товары, которые есть в наличии."""
        return self._collection.filter(lambda item: item.stock > 0)

    def filter_by_price(self, min_price: float, max_price: float) -> list[ProductItem]:
        """Отфильтровать товары по диапазону цен."""
        if min_price < 0 or max_price < 0:
            raise ValueError('Цена не может быть отрицательной')

        if min_price > max_price:
            raise ValueError('Минимальная цена не может быть больше максимальной')

        return self._collection.filter(
            lambda item: min_price <= item.price <= max_price
        )

    def remove_by_name(self, name: str) -> None:
        """Удалить товар по названию."""
        item = self.find_by_name(name)
        self._collection.remove(item)
        self._added_at.pop(item.name, None)

    def sort_items(self, strategy: str) -> list[ProductItem]:
        """Отсортировать товары по выбранной стратегии."""
        items = self._collection.get_all()

        if strategy == 'name':
            return sorted(items, key=lambda item: normalize(item.name))

        if strategy == 'price':
            return sorted(items, key=lambda item: item.price)

        if strategy == 'added_at':
            return sorted(items, key=lambda item: self._added_at.get(item.name, ''))

        raise ValueError('Неизвестная стратегия сортировки')

    def get_added_at(self, item: ProductItem) -> str:
        """Вернуть дату добавления товара."""
        return self._added_at.get(item.name, 'неизвестно')

    def count(self) -> int:
        """Вернуть количество товаров в коллекции."""
        return len(self._collection)

    def _add_item(self, item: ProductItem) -> None:
        """Добавить товар в коллекцию и сохранить дату добавления."""
        try:
            self._collection.add(item)
        except ValueError as error:
            raise DuplicateItemError(str(error)) from error

        self._added_at[item.name] = self._now()

    def _now(self) -> str:
        """Вернуть текущую дату и время в строковом формате."""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')