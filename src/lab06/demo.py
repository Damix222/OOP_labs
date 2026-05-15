from src.lab04.models import DigitalProduct, Service, Accessory
from src.lab06.container import TypedCollection, Displayable, Scorable


def print_collection(collection):
    for item in collection:
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

    digital_3 = DigitalProduct(
        name='Photo Editor',
        price=5200,
        stock=0,
        category='ПО',
        discount=15,
        file_size_mb=1200,
        license_type='Стандартная'
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

    digital_items = [
        digital_1,
        digital_2,
        digital_3,
    ]

    all_items = [
        digital_1,
        digital_2,
        digital_3,
        service_1,
        service_2,
        accessory_1,
        accessory_2,
    ]

    digital_collection: TypedCollection[DigitalProduct] = TypedCollection(DigitalProduct)

    for item in digital_items:
        digital_collection.add(item)

    print('=' * 70)
    print('СЦЕНАРИЙ 1. Типизированная коллекция DigitalProduct')
    print('=' * 70)
    print_collection(digital_collection)

    print('\n' + '=' * 70)
    print('СЦЕНАРИЙ 2. get_all() и проверка типа при добавлении')
    print('=' * 70)

    print('\n--- Получение всех элементов через get_all() ---')
    for product in digital_collection.get_all():
        print(product.name)

    print('\n--- Попытка добавить Service в TypedCollection[DigitalProduct] ---')
    try:
        digital_collection.add(service_1)  # type: ignore[arg-type]
    except TypeError as error:
        print(f'Ошибка: {error}')

    print('\n' + '=' * 70)
    print('СЦЕНАРИЙ 3. Метод find()')
    print('=' * 70)

    print('\n--- Найти товар дороже 5000 руб. ---')
    found_product = digital_collection.find(lambda item: item.price > 5000)
    print(found_product.name if found_product is not None else None)

    print('\n--- Найти несуществующий товар ---')
    not_found_product = digital_collection.find(
        lambda item: item.name == 'Несуществующий товар'
    )
    print(not_found_product)

    print('\n' + '=' * 70)
    print('СЦЕНАРИЙ 4. Метод filter()')
    print('=' * 70)

    print('\n--- Только товары в наличии ---')
    available_products = digital_collection.filter(lambda item: item.stock > 0)
    print_list(product.name for product in available_products)

    print('\n--- Только дорогие товары ---')
    expensive_products = digital_collection.filter(lambda item: item.price >= 5000)
    print_list(product.name for product in expensive_products)

    print('\n' + '=' * 70)
    print('СЦЕНАРИЙ 5. Метод map() и изменение типа результата')
    print('=' * 70)

    names: list[str] = digital_collection.map(lambda item: item.name)
    totals: list[float] = digital_collection.map(lambda item: item.calculate_total())

    print('\n--- map() -> list[str] с названиями ---')
    print_list(names)
    print(f'Тип первого элемента: {type(names[0]).__name__}')

    print('\n--- map() -> list[float] с итоговыми ценами ---')
    for total in totals:
        print(f'{total:.2f} руб.')
    print(f'Тип первого элемента: {type(totals[0]).__name__}')

    print('\n' + '=' * 70)
    print('СЦЕНАРИЙ 6. Protocol Displayable')
    print('=' * 70)

    displayable_collection: TypedCollection[Displayable] = TypedCollection(Displayable)

    for item in all_items:
        displayable_collection.add(item)

    print('\n--- Объекты разных классов без наследования от Protocol ---')
    print_collection(displayable_collection)

    print('\n--- Вызов display() для каждого объекта ---')
    display_texts = displayable_collection.display_all()
    print_list(display_texts)

    print('\n' + '=' * 70)
    print('СЦЕНАРИЙ 7. Protocol Scorable')
    print('=' * 70)

    scorable_collection: TypedCollection[Scorable] = TypedCollection(Scorable)

    for item in all_items:
        scorable_collection.add(item)

    print('\n--- Вызов score() для каждого объекта ---')
    scores = scorable_collection.score_all()

    for item, score in zip(all_items, scores):
        print(f'{item.name}: {score:.2f} руб.')

    print('\n' + '=' * 70)
    print('СЦЕНАРИЙ 8. Один TypedCollection с разными ограничениями')
    print('=' * 70)

    print('\n--- TypedCollection[Displayable] выводит строки display() ---')
    print_list(displayable_collection.map(lambda item: item.display().split('\n')[0]))

    print('\n--- TypedCollection[Scorable] возвращает числовые оценки score() ---')
    score_values: list[float] = scorable_collection.map(lambda item: item.score())
    for value in score_values:
        print(f'{value:.2f} руб.')


if __name__ == '__main__':
    main()
