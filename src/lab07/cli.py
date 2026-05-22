from __future__ import annotations

from src.lab07.app import ShopApp
from src.lab07.exceptions import DuplicateItemError, ItemNotFoundError, StorageError
from src.lab07.storage import ProductItem


class ShopCLI:
    """Консольный интерфейс приложения магазина."""

    def __init__(self, app: ShopApp) -> None:
        """Создать CLI и связать его с приложением."""
        self._app = app

    def run(self) -> None:
        """Запустить главный цикл приложения."""
        self._load_on_start()

        while True:
            self._print_menu()
            choice = self._read_int('Выберите пункт: ')

            if choice is None:
                print('Ошибка: введите число')
                continue

            if choice == 1:
                self._add_item_menu()
            elif choice == 2:
                self._show_items(self._app.get_all_items())
            elif choice == 3:
                self._find_item_menu()
            elif choice == 4:
                self._filter_menu()
            elif choice == 5:
                self._sort_menu()
            elif choice == 6:
                self._remove_item_menu()
            elif choice == 0:
                self._save_on_exit()
                print('Программа завершена')
                break
            else:
                print('Ошибка: такого пункта меню нет')

    def _load_on_start(self) -> None:
        """Загрузить данные при запуске приложения."""
        try:
            self._app.load_data()
            print(f'Данные загружены.\nОбъектов в коллекции: {self._app.count()}')
        except StorageError as error:
            print(f'Ошибка загрузки: {error}')

    def _save_on_exit(self) -> None:
        """Сохранить данные перед выходом."""
        try:
            self._app.save_data()
            print('Данные сохранены')
        except StorageError as error:
            print(f'Ошибка сохранения: {error}')

    def _print_menu(self) -> None:
        """Вывести главное меню."""
        print('\n' + '=' * 60)
        print('МАГАЗИН ЭЛЕКТРОНИКИ — CLI')
        print('=' * 60)
        print('1. Добавить товар')
        print('2. Показать все товары')
        print('3. Найти товар по названию')
        print('4. Фильтрация')
        print('5. Сортировка')
        print('6. Удалить товар')
        print('0. Сохранить и выйти')

    def _add_item_menu(self) -> None:
        """Показать меню добавления товара."""
        print('\nТип товара:')
        print('1. Обычный товар')
        print('2. Цифровой товар')
        print('3. Услуга')
        print('4. Аксессуар')

        choice = self._read_int('Выберите тип: ')

        if choice is None:
            print('Ошибка: введите число')
            return

        try:
            if choice == 1:
                self._add_product()
            elif choice == 2:
                self._add_digital_product()
            elif choice == 3:
                self._add_service()
            elif choice == 4:
                self._add_accessory()
            else:
                print('Ошибка: неизвестный тип товара')
        except (ValueError, TypeError, DuplicateItemError) as error:
            print(f'Ошибка: {error}')

    def _add_product(self) -> None:
        """Считать данные и добавить обычный товар."""
        name, price, stock, category, discount = self._read_base_product_data()

        self._app.add_product(
            name=name,
            price=price,
            stock=stock,
            category=category,
            discount=discount,
        )

        print('Обычный товар добавлен')

    def _add_digital_product(self) -> None:
        """Считать данные и добавить цифровой товар."""
        name, price, stock, category, discount = self._read_base_product_data()
        file_size_mb = self._read_float_required('Размер файла в МБ: ')
        license_type = input('Тип лицензии: ')

        self._app.add_digital_product(
            name=name,
            price=price,
            stock=stock,
            category=category,
            discount=discount,
            file_size_mb=file_size_mb,
            license_type=license_type,
        )

        print('Цифровой товар добавлен')

    def _add_service(self) -> None:
        """Считать данные и добавить услугу."""
        name, price, stock, category, discount = self._read_base_product_data()
        duration_hours = self._read_float_required('Длительность в часах: ')
        on_site = self._read_bool('Выезд мастера? y/n: ')

        self._app.add_service(
            name=name,
            price=price,
            stock=stock,
            category=category,
            discount=discount,
            duration_hours=duration_hours,
            on_site=on_site,
        )

        print('Услуга добавлена')

    def _add_accessory(self) -> None:
        """Считать данные и добавить аксессуар."""
        name, price, stock, category, discount = self._read_base_product_data()
        compatibility = input('Совместимость: ')
        wireless = self._read_bool('Беспроводной? y/n: ')

        self._app.add_accessory(
            name=name,
            price=price,
            stock=stock,
            category=category,
            discount=discount,
            compatibility=compatibility,
            wireless=wireless,
        )

        print('Аксессуар добавлен')

    def _read_base_product_data(self) -> tuple[str, float, int, str, float]:
        """Считать общие данные товара."""
        name = input('Название: ')
        price = self._read_float_required('Цена: ')
        stock = self._read_int_required('Остаток: ')
        category = input('Категория: ')
        discount = self._read_float_required('Скидка: ')

        return name, price, stock, category, discount

    def _find_item_menu(self) -> None:
        """Найти товар по названию и вывести результат."""
        name = input('Введите название: ')

        try:
            item = self._app.find_by_name(name)
            self._show_items([item])
        except ItemNotFoundError as error:
            print(f'Ошибка: {error}')

    def _filter_menu(self) -> None:
        """Показать меню фильтрации."""
        print('\nФильтрация:')
        print('1. Только товары в наличии')
        print('2. По диапазону цен')

        choice = self._read_int('Выберите пункт: ')

        if choice is None:
            print('Ошибка: введите число')
            return

        try:
            if choice == 1:
                self._show_items(self._app.filter_available())
            elif choice == 2:
                min_price = self._read_float_required('Минимальная цена: ')
                max_price = self._read_float_required('Максимальная цена: ')
                self._show_items(self._app.filter_by_price(min_price, max_price))
            else:
                print('Ошибка: такого пункта фильтрации нет')
        except ValueError as error:
            print(f'Ошибка: {error}')

    def _sort_menu(self) -> None:
        """Показать меню сортировки."""
        print('\nСортировать по:')
        print('1. Названию')
        print('2. Цене')
        print('3. Дате добавления')

        choice = self._read_int('Выберите пункт: ')

        if choice is None:
            print('Ошибка: введите число')
            return

        strategy_by_choice = {
            1: 'name',
            2: 'price',
            3: 'added_at',
        }

        strategy = strategy_by_choice.get(choice)

        if strategy is None:
            print('Ошибка: такого пункта сортировки нет')
            return

        self._show_items(self._app.sort_items(strategy))

    def _remove_item_menu(self) -> None:
        """Удалить товар после подтверждения пользователя."""
        name = input('Введите название для удаления: ')

        try:
            item = self._app.find_by_name(name)
        except ItemNotFoundError as error:
            print(f'Ошибка: {error}')
            return

        if not self._confirm(f'Удалить "{item.name}"? y/n: '):
            print('Удаление отменено')
            return

        self._app.remove_by_name(name)
        print('Товар удалён')

    def _show_items(self, items: list[ProductItem]) -> None:
        """Вывести список товаров в виде таблицы."""
        if not items:
            print('Список пуст')
            return

        print('\n' + '-' * 118)
        print(
            f'{"№":<4}'
            f'{"Тип":<14}'
            f'{"Название":<24}'
            f'{"Категория":<16}'
            f'{"Цена":>10}'
            f'{"Остаток":>10}'
            f'{"Активен":>10}'
            f'{"Добавлен":>22}'
        )
        print('-' * 118)

        for index, item in enumerate(items, start=1):
            print(
                f'{index:<4}'
                f'{self._get_item_type(item):<14.14}'
                f'{item.name:<24.24}'
                f'{item.category:<16.16}'
                f'{item.price:>10.2f}'
                f'{item.stock:>10}'
                f'{str(item.is_active):>10}'
                f'{self._app.get_added_at(item):>22}'
            )

        print('-' * 118)

    def _get_item_type(self, item: ProductItem) -> str:
        """Вернуть название типа товара для таблицы."""
        class_name = item.__class__.__name__

        if class_name == 'Product':
            return 'Обычный'

        if class_name == 'DigitalProduct':
            return 'Цифровой'

        if class_name == 'Service':
            return 'Услуга'

        if class_name == 'Accessory':
            return 'Аксессуар'

        return class_name

    def _read_int(self, prompt: str) -> int | None:
        """Считать целое число или вернуть None."""
        try:
            return int(input(prompt))
        except ValueError:
            return None

    def _read_int_required(self, prompt: str) -> int:
        """Считать обязательное целое число."""
        value = self._read_int(prompt)

        if value is None:
            raise ValueError('нужно ввести целое число')

        return value

    def _read_float_required(self, prompt: str) -> float:
        """Считать обязательное вещественное число."""
        try:
            return float(input(prompt))
        except ValueError as error:
            raise ValueError('нужно ввести число') from error

    def _read_bool(self, prompt: str) -> bool:
        """Считать логическое значение в формате y/n."""
        value = input(prompt).strip().lower()

        if value in ('y', 'yes', 'д', 'да'):
            return True

        if value in ('n', 'no', 'н', 'нет'):
            return False

        raise ValueError('нужно ввести y или n')

    def _confirm(self, prompt: str) -> bool:
        """Считать подтверждение действия."""
        try:
            return self._read_bool(prompt)
        except ValueError:
            return False