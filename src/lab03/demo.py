from src.lab02.collection import ProductCatalog
from src.lab03.base import Product
from src.lab03.models import DigitalProduct, Service, Accessory


def print_title(title):
    print(f'\n--- {title} ---')
catalog = ProductCatalog()

mouse = Product(
    name='Игровая мышь',
    price=3500,
    stock=10,
    category='Периферия',
    discount=10
)

windows = DigitalProduct(
    name='Windows 11 Pro',
    price=12000,
    stock=50,
    category='ПО',
    discount=15,
    file_size_mb=6200,
    license_type='OEM'
)

repair = Service(
    name='Настройка ноутбука',
    price=2500,
    stock=5,
    category='Услуги',
    discount=0,
    duration_hours=2,
    on_site=True
)

headphones = Accessory(
    name='Беспроводные наушники',
    price=4500,
    stock=8,
    category='Аксессуары',
    discount=5,
    compatibility='Смартфон, ноутбук',
    wireless=True
)

catalog.add(mouse)
catalog.add(windows)
catalog.add(repair)
catalog.add(headphones)


# Сценарий 1. Создание и вывод объектов разных типов
print_title('Все объекты')
for item in catalog:
    print(item)
    print('-' * 40)


# Сценарий 2. Методы базового и дочерних классов
print_title('Методы')
print(f'{mouse.name}: финальная цена = {mouse.final_price():.2f} руб.')
print(windows.activate_license())
print(repair.book_service())
print(headphones.connect())


# Сценарий 3. Полиморфизм через calculate_total()
print_title('Полиморфизм')
for item in catalog:
    print(f'{item.name}: {item.calculate_total():.2f} руб.')


# Сценарий 4. Проверка типов через isinstance()
print_title('Проверка типов')
for item in catalog:
    if isinstance(item, DigitalProduct):
        print(f'{item.name} -> это DigitalProduct')
    elif isinstance(item, Service):
        print(f'{item.name} -> это Service')
    elif isinstance(item, Accessory):
        print(f'{item.name} -> это Accessory')
    elif isinstance(item, Product):
        print(f'{item.name} -> это базовый Product')


# Сценарий 5. Фильтрация по типу
print_title('Только цифровые товары')
digital_only = catalog.get_only_digital()
print(digital_only)

print_title('Только услуги')
services_only = catalog.get_only_services()
print(services_only)

print_title('Только аксессуары')
accessories_only = catalog.get_by_type(Accessory)
for item in accessories_only:
    print(item)
    print('-' * 40)


# Сценарий 6. Работа базовых методов у наследников
print_title('Покупка и пополнение')
mouse.buy(2)
repair.add_stock(3)
headphones.buy(1)

print(f'{mouse.name}: остаток {mouse.stock}')
print(f'{repair.name}: остаток {repair.stock}')
print(f'{headphones.name}: остаток {headphones.stock}')


print_title('Фильтрация аксессуаров через get_by_type')
accessories = catalog.get_by_type(Accessory)
for item in accessories:
    print(item.name)