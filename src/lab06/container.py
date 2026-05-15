from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import Any, Generic, Protocol, TypeVar, runtime_checkable

from src.lib.normalize import normalize


T = TypeVar('T')
R = TypeVar('R')


@runtime_checkable
class Displayable(Protocol):
    def display(self) -> str:
        ...


@runtime_checkable
class Scorable(Protocol):
    def score(self) -> float:
        ...


D = TypeVar('D', bound=Displayable)
S = TypeVar('S', bound=Scorable)


class TypedCollection(Generic[T]):
    """
    Generic-версия коллекции из ЛР-2.

    T — тип объектов, которые хранятся внутри коллекции.
    item_type нужен для runtime-проверки типа при добавлении.
    """

    def __init__(self, item_type: type[Any] | tuple[type[Any], ...] | None = None) -> None:
        self._items: list[T] = []
        self._item_type: type[Any] | tuple[type[Any], ...] | None = item_type

    def _type_name(self) -> str:
        if self._item_type is None:
            return 'любой тип'

        if isinstance(self._item_type, tuple):
            return ', '.join(item.__name__ for item in self._item_type)

        return self._item_type.__name__

    def _validate_item_type(self, item: T) -> None:
        if self._item_type is not None and not isinstance(item, self._item_type):
            raise TypeError(
                f'В коллекцию можно добавлять только объекты типа {self._type_name()}'
            )

    def _create_from_items(self, items: Iterable[T]) -> TypedCollection[T]:
        result: TypedCollection[T] = TypedCollection(self._item_type)

        for item in items:
            result.add(item)

        return result

    def _get_required_str_attr(self, item: T, attr_name: str) -> str:
        value = getattr(item, attr_name, None)

        if not isinstance(value, str):
            raise TypeError(f'У объекта нет строкового атрибута {attr_name}')

        return value

    def _get_required_number_attr(self, item: T, attr_name: str) -> int | float:
        value = getattr(item, attr_name, None)

        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f'У объекта нет числового атрибута {attr_name}')

        return value

    def add(self, item: T) -> None:
        self._validate_item_type(item)

        if hasattr(item, 'name'):
            new_name = normalize(self._get_required_str_attr(item, 'name'))

            for existing_item in self._items:
                if hasattr(existing_item, 'name'):
                    existing_name = normalize(
                        self._get_required_str_attr(existing_item, 'name')
                    )

                    if existing_name == new_name:
                        raise ValueError(
                            f"Объект с названием '{self._get_required_str_attr(item, 'name')}' уже есть в коллекции"
                        )

        self._items.append(item)

    def remove(self, item: T) -> None:
        self._validate_item_type(item)

        if item not in self._items:
            raise ValueError('Такого объекта нет в коллекции')

        self._items.remove(item)

    def remove_at(self, index: int) -> None:
        if isinstance(index, bool) or not isinstance(index, int):
            raise TypeError('Индекс должен быть целым числом')

        if index < 0 or index >= len(self._items):
            raise IndexError('Индекс вне диапазона')

        del self._items[index]

    def get_all(self) -> list[T]:
        return self._items.copy()

    def find_by_name(self, name: str) -> T | None:
        search_name = normalize(name)

        for item in self._items:
            item_name = getattr(item, 'name', None)

            if isinstance(item_name, str) and normalize(item_name) == search_name:
                return item

        return None

    def find_by_category(self, category: str) -> TypedCollection[T]:
        search_category = normalize(category)
        result: TypedCollection[T] = TypedCollection(self._item_type)

        for item in self._items:
            item_category = getattr(item, 'category', None)

            if isinstance(item_category, str) and normalize(item_category) == search_category:
                result.add(item)

        return result

    def sort_by_name(self, reverse: bool = False) -> TypedCollection[T]:
        sorted_items = sorted(
            self._items,
            key=lambda item: normalize(self._get_required_str_attr(item, 'name')),
            reverse=reverse,
        )

        return self._create_from_items(sorted_items)

    def sort_by_price(self, reverse: bool = False) -> TypedCollection[T]:
        sorted_items = sorted(
            self._items,
            key=lambda item: self._get_required_number_attr(item, 'price'),
            reverse=reverse,
        )

        return self._create_from_items(sorted_items)

    def sort_by_sortable(self, reverse: bool = False) -> TypedCollection[T]:
        from src.lab04.interfaces import Sortable

        sortable_items = []

        for item in self._items:
            if isinstance(item, Sortable):
                sortable_items.append(item)

        sorted_items = sorted(
            sortable_items,
            key=lambda item: item.sort_key(),
            reverse=reverse,
        )

        return self._create_from_items(sorted_items)

    def get_active(self) -> TypedCollection[T]:
        result: TypedCollection[T] = TypedCollection(self._item_type)

        for item in self._items:
            if getattr(item, 'is_active', False):
                result.add(item)

        return result

    def get_available(self) -> TypedCollection[T]:
        result: TypedCollection[T] = TypedCollection(self._item_type)

        for item in self._items:
            stock = getattr(item, 'stock', 0)

            if isinstance(stock, int) and stock > 0:
                result.add(item)

        return result

    def get_expensive(self, min_price: int | float) -> TypedCollection[T]:
        if isinstance(min_price, bool) or not isinstance(min_price, (int, float)):
            raise TypeError('Минимальная цена должна быть числом')

        result: TypedCollection[T] = TypedCollection(self._item_type)

        for item in self._items:
            price = getattr(item, 'price', None)

            if isinstance(price, (int, float)) and not isinstance(price, bool):
                if price >= min_price:
                    result.add(item)

        return result

    def get_by_type(self, item_type: type[Any]) -> TypedCollection[T]:
        if not isinstance(item_type, type):
            raise TypeError('Нужно передать класс или интерфейс')

        result: TypedCollection[T] = TypedCollection(self._item_type)

        for item in self._items:
            if isinstance(item, item_type):
                result.add(item)

        return result

    def get_only_digital(self) -> TypedCollection[T]:
        from src.lab03.models import DigitalProduct

        return self.get_by_type(DigitalProduct)

    def get_only_services(self) -> TypedCollection[T]:
        from src.lab03.models import Service

        return self.get_by_type(Service)

    def get_only_accessories(self) -> TypedCollection[T]:
        from src.lab03.models import Accessory

        return self.get_by_type(Accessory)

    def get_by_interface(self, interface_type: type[Any]) -> TypedCollection[T]:
        if not isinstance(interface_type, type):
            raise TypeError('Нужно передать интерфейс')

        return self.get_by_type(interface_type)

    def get_printable(self) -> TypedCollection[T]:
        from src.lab04.interfaces import Printable

        return self.get_by_interface(Printable)

    def get_actionable(self) -> TypedCollection[T]:
        from src.lab04.interfaces import Actionable

        return self.get_by_interface(Actionable)

    def get_sortable(self) -> TypedCollection[T]:
        from src.lab04.interfaces import Sortable

        return self.get_by_interface(Sortable)

    def find(self, predicate: Callable[[T], bool]) -> T | None:
        if not callable(predicate):
            raise TypeError('predicate должен быть вызываемым объектом')

        for item in self._items:
            if predicate(item):
                return item

        return None

    def filter(self, predicate: Callable[[T], bool]) -> list[T]:
        if not callable(predicate):
            raise TypeError('predicate должен быть вызываемым объектом')

        return [item for item in self._items if predicate(item)]

    def map(self, transform: Callable[[T], R]) -> list[R]:
        if not callable(transform):
            raise TypeError('transform должен быть вызываемым объектом')

        return [transform(item) for item in self._items]

    def display_all(self: TypedCollection[D]) -> list[str]:
        return [item.display() for item in self._items]

    def score_all(self: TypedCollection[S]) -> list[float]:
        return [item.score() for item in self._items]

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)

    def __getitem__(self, index: int) -> T:
        return self._items[index]

    def __str__(self) -> str:
        if not self._items:
            return 'Коллекция пуста'

        lines: list[str] = []

        for i, item in enumerate(self._items, start=1):
            name = getattr(item, 'name', 'без названия')
            category = getattr(item, 'category', 'без категории')
            price = getattr(item, 'price', None)
            stock = getattr(item, 'stock', None)
            is_active = getattr(item, 'is_active', None)

            price_text = f'{price:.2f}' if isinstance(price, (int, float)) else 'нет цены'
            stock_text = str(stock) if isinstance(stock, int) else 'нет остатка'
            active_text = str(is_active) if isinstance(is_active, bool) else 'неизвестно'

            lines.append(
                f'{i}. {name} | {category} | '
                f'Цена: {price_text} | Остаток: {stock_text} | '
                f'Активен: {active_text}'
            )

        return '\n'.join(lines)