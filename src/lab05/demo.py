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


def print_title(title):
    print('\n' + '=' * 70)
    print(title)
    print('=' * 70)


def print_catalog(title, catalog):
    print_title(title)
    print(catalog)


def print_list(title, items):
    print_title(title)

    if not items:
        print('Список пуст')
        return

    for i, item in enumerate(items, start=1):
        print(f'{i}. {item}')


def create_catalog():
    catalog = ProductCatalog()

    catalog.add(
        DigitalProduct(
            name='Windows 11 Pro',
            price=12000,
            stock=5,
            category='ПО',
            discount=10,
            file_size_mb=5000,
            license_type='Профессиональная'
        )
    )

    catalog.add(
        DigitalProduct(
            name='Антивирус Pro',
            price=3500,
            stock=15,
            category='ПО',
            discount=5,
            file_size_mb=250,
            license_type='Годовая'
        )
    )

    catalog.add(
        Service(
            name='Настройка ноутбука',
            price=2500,
            stock=10,
            category='Услуги',
            discount=0,
            duration_hours=2,
            on_site=True
        )
    )

    catalog.add(
        Service(
            name='Чистка системы',
            price=1800,
            stock=0,
            category='Услуги',
            discount=0,
            duration_hours=1.5,
            on_site=False
        )
    )

    catalog.add(
        Accessory(
            name='Беспроводная мышь',
            price=2400,
            stock=20,
            category='Аксессуары',
            discount=15,
            compatibility='ПК и ноутбук',
            wireless=True
        )
    )

    catalog.add(
        Accessory(
            name='USB-C кабель',
            price=800,
            stock=35,
            category='Аксессуары',
            discount=0,
            compatibility='USB-C устройства',
            wireless=False
        )
    )

    return catalog


def scenario_sorting(catalog):
    print_catalog(
        'Сортировка по названию',
        catalog.sort_by(by_name)
    )

    print_catalog(
        'Сортировка по цене',
        catalog.sort_by(by_price)
    )

    print_catalog(
        'Сортировка по категории и названию',
        catalog.sort_by(by_category_and_name)
    )


def scenario_filtering(catalog):
    print_catalog(
        'Фильтрация: только товары в наличии',
        catalog.filter_by(is_available)
    )

    print_catalog(
        'Фильтрация: дорогие товары',
        catalog.filter_by(is_expensive)
    )

    print_catalog(
        'Фильтрация: только цифровые товары',
        catalog.filter_by(is_digital_product)
    )


def scenario_map_and_factory(catalog):
    names = list(map(get_name, catalog))

    print_list(
        'map(): получение названий товаров',
        names
    )

    short_strings = list(map(to_short_string, catalog))

    print_list(
        'map(): преобразование товаров в строки',
        short_strings
    )

    dicts = list(map(to_dict, catalog))

    print_list(
        'map(): преобразование товаров в словари',
        dicts
    )

    cheap_filter = make_price_filter(3000)

    print_catalog(
        'Фабрика функций: товары дешевле или равные 3000 руб.',
        catalog.filter_by(cheap_filter)
    )

    software_filter = make_category_filter('по')

    print_catalog(
        'Фабрика функций с normalize(): товары из категории ПО',
        catalog.filter_by(software_filter)
    )

    discount_20 = make_discount_function(20)

    print_list(
        'Фабрика функций: расчёт цены с дополнительной скидкой 20%',
        catalog.apply(discount_20)
    )


def scenario_lambda_vs_named_function(catalog):
    named_result = catalog.sort_by(by_name)

    lambda_result = catalog.sort_by(
        lambda item: normalize(item.name)
    )

    print_catalog(
        'Сортировка через именованную функцию by_name',
        named_result
    )

    print_catalog(
        'Та же сортировка через lambda',
        lambda_result
    )


def scenario_chain(catalog):
    print_title('Сценарий 1: цепочка filter → sort → apply')

    step_1 = catalog.filter_by(is_available)
    print('\nШаг 1. Оставили только товары в наличии:')
    print(step_1)

    step_2 = step_1.sort_by(by_price)
    print('\nШаг 2. Отсортировали товары по цене:')
    print(step_2)

    discount_strategy = DiscountStrategy(10)
    step_3 = step_2.apply(discount_strategy)

    print('\nШаг 3. Применили стратегию дополнительной скидки 10%:')
    for i, price in enumerate(step_3, start=1):
        print(f'{i}. Цена после дополнительной скидки: {price:.2f} руб.')

    result = (
        catalog
        .filter_by(is_available)
        .sort_by(by_price)
        .apply(discount_strategy)
    )

    print('\nИтог той же цепочки в одной записи:')
    for i, price in enumerate(result, start=1):
        print(f'{i}. {price:.2f} руб.')


def scenario_strategy_replacement(catalog):
    print_title('Сценарий 2: замена стратегии без изменения кода коллекции')

    price_sorted = catalog.sort_by(by_price)

    print('\nСтратегия 1: сортировка по обычной цене')
    print(price_sorted)

    total_price_sorted = catalog.sort_by(by_total_price)

    print('\nСтратегия 2: сортировка по итоговой стоимости')
    print(total_price_sorted)

    category_sorted = catalog.sort_by(by_category_and_name)

    print('\nСтратегия 3: сортировка по категории и названию')
    print(category_sorted)


def scenario_callable_object(catalog):
    print_title('Сценарий 3: callable-объекты как стратегии')

    discount_10 = DiscountStrategy(10)
    discount_25 = DiscountStrategy(25)
    total_price_strategy = TotalPriceStrategy()
    short_info_strategy = ShortInfoStrategy()

    print('\nDiscountStrategy(10):')
    prices_10 = catalog.apply(discount_10)

    for i, price in enumerate(prices_10, start=1):
        print(f'{i}. {price:.2f} руб.')

    print('\nDiscountStrategy(25):')
    prices_25 = catalog.apply(discount_25)

    for i, price in enumerate(prices_25, start=1):
        print(f'{i}. {price:.2f} руб.')

    print('\nTotalPriceStrategy():')
    totals = catalog.apply(total_price_strategy)

    for i, price in enumerate(totals, start=1):
        print(f'{i}. {price:.2f} руб.')

    print('\nShortInfoStrategy():')
    info = catalog.apply(short_info_strategy)

    for i, text in enumerate(info, start=1):
        print(f'{i}. {text}')


def main():
    catalog = create_catalog()

    print_catalog(
        'Исходная коллекция товаров',
        catalog
    )

    scenario_sorting(catalog)
    scenario_filtering(catalog)
    scenario_map_and_factory(catalog)
    scenario_lambda_vs_named_function(catalog)
    scenario_chain(catalog)
    scenario_strategy_replacement(catalog)
    scenario_callable_object(catalog)


if __name__ == '__main__':
    main()