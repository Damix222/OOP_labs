from src.lib.normalize import normalize
from src.lab04.models import DigitalProduct, Service, Accessory
from src.lab05.collection import ProductCatalog
from src.lab05.strategies import (
    by_name,
    by_price,
    by_category_and_name,
    by_total_price,
    is_available,
    is_expensive,
    is_digital_product,
    get_name,
    to_short_string,
    to_dict,
    make_price_filter,
    make_category_filter,
    make_discount_function,
    DiscountStrategy,
    TotalPriceStrategy,
    ShortInfoStrategy,
)


def print_catalog(catalog):
    for item in catalog:
        print(
            f'{item.name} | '
            f'{item.category} | '
            f'Цена: {item.price:.2f} руб. | '
            f'Остаток: {item.stock} | '
            f'Активен: {item.is_active}'
        )


def print_list(items):
    for item in items:
        print(item)


def main():
    digital_1 = DigitalProduct(
        name='Windows 11 Pro',
        price=12000,
        stock=5,
        category='ПО',
        discount=10,
        file_size_mb=5000,
        license_type='Профессиональная'
    )

    digital_2 = DigitalProduct(
        name='Антивирус Pro',
        price=3500,
        stock=15,
        category='ПО',
        discount=5,
        file_size_mb=250,
        license_type='Годовая'
    )

    service_1 = Service(
        name='Настройка ноутбука',
        price=2500,
        stock=10,
        category='Услуги',
        discount=0,
        duration_hours=2,
        on_site=True
    )

    service_2 = Service(
        name='Чистка системы',
        price=1800,
        stock=0,
        category='Услуги',
        discount=0,
        duration_hours=1.5,
        on_site=False
    )

    accessory_1 = Accessory(
        name='Беспроводная мышь',
        price=2400,
        stock=20,
        category='Аксессуары',
        discount=15,
        compatibility='ПК и ноутбук',
        wireless=True
    )

    accessory_2 = Accessory(
        name='USB-C кабель',
        price=800,
        stock=35,
        category='Аксессуары',
        discount=0,
        compatibility='USB-C устройства',
        wireless=False
    )

    items = [
        digital_1,
        digital_2,
        service_1,
        service_2,
        accessory_1,
        accessory_2,
    ]

    catalog = ProductCatalog()

    for item in items:
        catalog.add(item)

    print('=' * 70)
    print('СЦЕНАРИЙ 1. Исходная коллекция товаров')
    print('=' * 70)
    print_catalog(catalog)

    print('\n' + '=' * 70)
    print('СЦЕНАРИЙ 2. Сортировка разными стратегиями')
    print('=' * 70)

    print('\n--- Сортировка по названию ---')
    print_catalog(catalog.sort_by(by_name))

    print('\n--- Сортировка по цене ---')
    print_catalog(catalog.sort_by(by_price))

    print('\n--- Сортировка по категории и названию ---')
    print_catalog(catalog.sort_by(by_category_and_name))

    print('\n' + '=' * 70)
    print('СЦЕНАРИЙ 3. Фильтрация коллекции')
    print('=' * 70)

    print('\n--- Только товары в наличии ---')
    print_catalog(catalog.filter_by(is_available))

    print('\n--- Только дорогие товары ---')
    print_catalog(catalog.filter_by(is_expensive))

    print('\n--- Только цифровые товары ---')
    print_catalog(catalog.filter_by(is_digital_product))

    print('\n' + '=' * 70)
    print('СЦЕНАРИЙ 4. Применение map()')
    print('=' * 70)

    names = list(map(get_name, catalog))
    print('\n--- Названия товаров ---')
    print_list(names)

    short_strings = list(map(to_short_string, catalog))
    print('\n--- Товары в виде строк ---')
    print_list(short_strings)

    dicts = list(map(to_dict, catalog))
    print('\n--- Товары в виде словарей ---')
    print_list(dicts)

    print('\n' + '=' * 70)
    print('СЦЕНАРИЙ 5. Использование фабрик функций')
    print('=' * 70)

    cheap_filter = make_price_filter(3000)
    print('\n--- Товары дешевле или равные 3000 руб. ---')
    print_catalog(catalog.filter_by(cheap_filter))

    software_filter = make_category_filter('по')
    print('\n--- Товары из категории ПО ---')
    print_catalog(catalog.filter_by(software_filter))

    discount_20 = make_discount_function(20)
    print('\n--- Цена с дополнительной скидкой 20% ---')
    prices_with_discount = catalog.apply(discount_20)

    for price in prices_with_discount:
        print(f'{price:.2f} руб.')

    print('\n' + '=' * 70)
    print('СЦЕНАРИЙ 6. Сравнение lambda и именованной функции')
    print('=' * 70)

    print('\n--- Сортировка через именованную функцию by_name ---')
    print_catalog(catalog.sort_by(by_name))

    print('\n--- Такая же сортировка через lambda ---')
    print_catalog(catalog.sort_by(lambda item: normalize(item.name)))

    print('\n' + '=' * 70)
    print('СЦЕНАРИЙ 7. Цепочка filter → sort → apply')
    print('=' * 70)

    discount_10 = DiscountStrategy(10)

    result = (
        catalog
        .filter_by(is_available)
        .sort_by(by_price)
        .apply(discount_10)
    )

    print('\n--- Итог после filter_by → sort_by → apply ---')
    for price in result:
        print(f'{price:.2f} руб.')

    print('\n' + '=' * 70)
    print('СЦЕНАРИЙ 8. Замена стратегии без изменения кода коллекции')
    print('=' * 70)

    print('\n--- Стратегия 1: сортировка по обычной цене ---')
    print_catalog(catalog.sort_by(by_price))

    print('\n--- Стратегия 2: сортировка по итоговой стоимости ---')
    print_catalog(catalog.sort_by(by_total_price))

    print('\n--- Стратегия 3: сортировка по категории и названию ---')
    print_catalog(catalog.sort_by(by_category_and_name))

    print('\n' + '=' * 70)
    print('СЦЕНАРИЙ 9. Callable-объекты как стратегии')
    print('=' * 70)

    discount_25 = DiscountStrategy(25)
    total_price_strategy = TotalPriceStrategy()
    short_info_strategy = ShortInfoStrategy()

    print('\n--- DiscountStrategy(25) ---')
    discounted_prices = catalog.apply(discount_25)

    for price in discounted_prices:
        print(f'{price:.2f} руб.')

    print('\n--- TotalPriceStrategy() ---')
    total_prices = catalog.apply(total_price_strategy)

    for price in total_prices:
        print(f'{price:.2f} руб.')

    print('\n--- ShortInfoStrategy() ---')
    short_info = catalog.apply(short_info_strategy)
    print_list(short_info)


if __name__ == '__main__':
    main()