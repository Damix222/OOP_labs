from src.lab01.model import Product
from src.lab02.collection import ProductCatalog


def main():
    laptop = Product('Ноутбук Lenovo', 80000, 5, 'Электроника', 10)
    mouse = Product('Мышь Logitech', 2500, 10, 'Аксессуары', 5)
    cable = Product('USB-кабель', 500, 0, 'Аксессуары', 0)
    monitor = Product('Монитор Samsung', 22000, 3, 'Электроника', 7)

    catalog = ProductCatalog()

    print('\nСценарий 1. Добавление товаров в каталог\n')
    catalog.add(laptop)
    catalog.add(mouse)
    catalog.add(cable)
    catalog.add(monitor)

    print(catalog)
    print()
    print('Количество товаров в каталоге:', len(catalog))
    print()

    print('\nСценарий 2. Поиск, цикл, индексация\n')

    found = catalog.find_by_name('Мышь Logitech')
    print('Результат поиска по названию:')
    print(found if found else 'Товар не найден')
    print()

    print('Перебор каталога через for:')
    for item in catalog:
        print(f'- {item.name}: {item.price:.2f} руб.')
    print()

    print('Индексация:')
    print(catalog[0])
    print()

    print('\nСценарий 3. Сортировка и фильтрация\n')

    print('Сортировка по цене:')
    sorted_by_price = catalog.sort_by_price()
    print(sorted_by_price)
    print()

    print('Только активные товары:')
    active_catalog = catalog.get_active()
    print(active_catalog)
    print()

    print('Товары дороже 10000:')
    expensive_catalog = catalog.get_expensive(10000)
    print(expensive_catalog)
    print()

    print('Только категория "Аксессуары":')
    accessories = catalog.find_by_category('Аксессуары')
    print(accessories)
    print()

    print('\nСценарий 4. Удаление товара\n')
    catalog.remove(mouse)
    print('После удаления мыши:')
    print(catalog)
    print()

    print('Удаление по индексу:')
    catalog.remove_at(0)
    print(catalog)
    print()

    print('\nСценарий 5. Проверки ограничений\n')

    try:
        catalog.add('не товар')
    except Exception as e:
        print('Ошибка при добавлении неправильного типа:', e)

    try:
        duplicate = Product('Монитор Samsung', 30000, 2, 'Электроника', 3)
        catalog.add(duplicate)
    except Exception as e:
        print('Ошибка при добавлении дубликата:', e)

    try:
        catalog.remove_at(100)
    except Exception as e:
        print('Ошибка при удалении по неверному индексу:', e)


if __name__ == '__main__':
    main()