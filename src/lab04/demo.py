from src.lab02.collections import ProductCatalog
from src.lab04.interfaces import Printable, Actionable, Sortable
from src.lab04.models import DigitalProduct, Service, Accessory


def print_all(items: list[Printable]):
    print('--- Вывод через интерфейс Printable ---')
    for item in items:
        print(item.to_string())


def run_all_actions(items: list[Actionable]):
    print('--- Действия через интерфейс Actionable ---')
    for item in items:
        print(item.do_action())


def show_sort_keys(items: list[Sortable]):
    print('--- Ключи сортировки через интерфейс Sortable ---')
    for item in items:
        print(f'{item.name}: {item.sort_key()}')


def main():
    digital = DigitalProduct(
        name='Windows 11 Pro',
        price=3500,
        stock=25,
        category='Программное обеспечение',
        discount=10,
        file_size_mb=5500,
        license_type='OEM'
    )

    service = Service(
        name='Настройка ноутбука',
        price=2000,
        stock=10,
        category='Сервис',
        discount=5,
        duration_hours=2,
        on_site=True
    )

    accessory = Accessory(
        name='Беспроводная мышь',
        price=1500,
        stock=40,
        category='Аксессуары',
        discount=15,
        compatibility='Ноутбук / ПК',
        wireless=True
    )

    items = [digital, service, accessory]

    catalog = ProductCatalog()
    for item in items:
        catalog.add(item)

    print('=' * 70)
    print('СЦЕНАРИЙ 1. Единый вывод объектов разных типов')
    print('=' * 70)
    print_all(items)

    print('\n' + '=' * 70)
    print('СЦЕНАРИЙ 2. Разные действия через единый интерфейс')
    print('=' * 70)
    run_all_actions(items)

    print('\n' + '=' * 70)
    print('СЦЕНАРИЙ 3. Проверка isinstance')
    print('=' * 70)
    for item in items:
        print(
            f'{item.name}: '
            f'Printable={isinstance(item, Printable)}, '
            f'Actionable={isinstance(item, Actionable)}, '
            f'Sortable={isinstance(item, Sortable)}'
        )

    print('\n' + '=' * 70)
    print('СЦЕНАРИЙ 4. Фильтрация коллекции по интерфейсам')
    print('=' * 70)
    printable_catalog = catalog.get_printable()
    actionable_catalog = catalog.get_actionable()
    sortable_catalog = catalog.get_sortable()

    print(f'Printable объектов: {len(printable_catalog)}')
    print(f'Actionable объектов: {len(actionable_catalog)}')
    print(f'Sortable объектов: {len(sortable_catalog)}')

    print('\nТолько Printable-объекты:')
    print_all(printable_catalog)

    print('\n' + '=' * 70)
    print('СЦЕНАРИЙ 5. Сортировка через интерфейс')
    print('=' * 70)
    sorted_catalog = catalog.sort_by_sortable()
    print_all(sorted_catalog)

    print('\n' + '=' * 70)
    print('СЦЕНАРИЙ 6. Показ ключей сортировки')
    print('=' * 70)
    show_sort_keys(items)


if __name__ == '__main__':
    main()