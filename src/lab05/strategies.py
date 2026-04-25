from src.lib.normalize import normalize
from src.lab03.models import DigitalProduct, Service, Accessory


def by_name(item):
    """Стратегия сортировки товара по названию."""
    return normalize(item.name)


def by_price(item):
    """Стратегия сортировки товара по обычной цене."""
    return item.price


def by_category_and_name(item):
    """Стратегия сортировки товара сначала по категории, затем по названию."""
    return (
        normalize(item.category),
        normalize(item.name)
    )


def by_total_price(item):
    """Стратегия сортировки товара по итоговой стоимости."""
    return item.calculate_total()


def is_available(item):
    """Фильтр: возвращает True, если товар есть в наличии."""
    return item.stock > 0


def is_active(item):
    """Фильтр: возвращает True, если товар активен."""
    return item.is_active


def is_expensive(item):
    """Фильтр: возвращает True, если цена товара не меньше 5000 рублей."""
    return item.price >= 5000


def is_digital_product(item):
    """Фильтр: возвращает True, если объект является цифровым товаром."""
    return isinstance(item, DigitalProduct)


def is_service(item):
    """Фильтр: возвращает True, если объект является услугой."""
    return isinstance(item, Service)


def is_accessory(item):
    """Фильтр: возвращает True, если объект является аксессуаром."""
    return isinstance(item, Accessory)


def get_name(item):
    """Преобразует объект товара в его название."""
    return item.name


def to_short_string(item):
    """Преобразует объект товара в короткую строку для вывода."""
    return (
        f'{item.name} | {item.category} | '
        f'Цена: {item.price:.2f} руб. | '
        f'Итог: {item.calculate_total():.2f} руб.'
    )


def to_dict(item):
    """Преобразует объект товара в словарь."""
    return {
        'name': item.name,
        'category': item.category,
        'price': item.price,
        'stock': item.stock,
        'active': item.is_active,
        'total': item.calculate_total(),
    }


def make_price_filter(max_price):
    """
    Фабрика функций.

    Создаёт и возвращает функцию-фильтр,
    которая оставляет товары с ценой не выше max_price.
    """
    if isinstance(max_price, bool) or not isinstance(max_price, (int, float)):
        raise TypeError('Максимальная цена должна быть числом')

    if max_price <= 0:
        raise ValueError('Максимальная цена должна быть больше 0')

    def filter_fn(item):
        return item.price <= max_price

    return filter_fn


def make_category_filter(category):
    """
    Фабрика функций.

    Создаёт и возвращает функцию-фильтр,
    которая оставляет товары из указанной категории.
    """
    search_category = normalize(category)

    def filter_fn(item):
        return normalize(item.category) == search_category

    return filter_fn


def make_discount_function(percent):
    """
    Фабрика функций.

    Создаёт функцию, которая считает цену товара
    с дополнительной скидкой.
    """
    if isinstance(percent, bool) or not isinstance(percent, (int, float)):
        raise TypeError('Скидка должна быть числом')

    if percent < 0 or percent > 100:
        raise ValueError('Скидка должна быть от 0 до 100')

    def discount_fn(item):
        return item.final_price() * (1 - percent / 100)

    return discount_fn


class DiscountStrategy:
    """
    Callable-объект для расчёта цены с дополнительной скидкой.

    Объект этого класса можно передавать туда же,
    куда передаётся обычная функция.
    """

    def __init__(self, percent):
        if isinstance(percent, bool) or not isinstance(percent, (int, float)):
            raise TypeError('Скидка должна быть числом')

        if percent < 0 or percent > 100:
            raise ValueError('Скидка должна быть от 0 до 100')

        self._percent = float(percent)

    def __call__(self, item):
        return item.final_price() * (1 - self._percent / 100)


class TotalPriceStrategy:
    """
    Callable-объект для получения итоговой стоимости товара.

    Использует полиморфный метод calculate_total().
    """

    def __call__(self, item):
        return item.calculate_total()


class ShortInfoStrategy:
    """
    Callable-объект для преобразования товара в короткую строку.
    """

    def __call__(self, item):
        return to_short_string(item)