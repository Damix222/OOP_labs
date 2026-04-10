from src.lab03.base import Product
from src.lib.normalize import normalize

def validate_text(value, field_name):
    if not isinstance(value, str):
        raise TypeError(f'{field_name} должно быть строкой')

    value = normalize(value, casefold=False, yo2e=False)

    if value == '':
        raise ValueError(f'{field_name} не должно быть пустым')

    return value


def validate_positive_number(value, field_name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f'{field_name} должно быть числом')

    if value <= 0:
        raise ValueError(f'{field_name} должно быть больше 0')

    return float(value)


def validate_bool(value, field_name):
    if not isinstance(value, bool):
        raise TypeError(f'{field_name} должно быть логическим значением')

    return value



class DigitalProduct(Product):
    def __init__(
        self,
        name,
        price,
        stock,
        category,
        discount=0,
        file_size_mb=1,
        license_type='Стандартная'
    ):
        super().__init__(name, price, stock, category, discount)
        self._file_size_mb = validate_positive_number(file_size_mb, 'Размер файла')
        self._license_type = validate_text(license_type, 'Тип лицензии')

    @property
    def file_size_mb(self):
        return self._file_size_mb

    @property
    def license_type(self):
        return self._license_type

    def activate_license(self):
        return (
            f"Лицензия для товара '{self.name}' активирована. "
            f"Тип лицензии: {self.license_type}"
        )

    def calculate_total(self):
        """
        Для цифрового товара делаем дополнительную онлайн-скидку 5%.
        Это нужно для демонстрации полиморфизма.
        """
        return self.final_price() * 0.95

    def __str__(self):
        return (
            f'{super().__str__()}\n'
            f'Тип товара: цифровой\n'
            f'Размер файла: {self.file_size_mb:.1f} МБ\n'
            f'Тип лицензии: {self.license_type}\n'
            f'Итоговая стоимость: {self.calculate_total():.2f} руб.'
        )

    def __repr__(self):
        return (
            f"DigitalProduct(name='{self.name}', price={self.price}, stock={self.stock}, "
            f"category='{self.category}', discount={self.discount}, "
            f"file_size_mb={self.file_size_mb}, license_type='{self.license_type}')"
        )


class Service(Product):
    def __init__(
        self,
        name,
        price,
        stock,
        category,
        discount=0,
        duration_hours=1,
        on_site=False
    ):
        super().__init__(name, price, stock, category, discount)
        self._duration_hours = validate_positive_number(duration_hours, 'Длительность')
        self._on_site = validate_bool(on_site, 'Выезд мастера')

    @property
    def duration_hours(self):
        return self._duration_hours

    @property
    def on_site(self):
        return self._on_site

    def book_service(self):
        return (
            f"Услуга '{self.name}' забронирована "
            f"на {self._duration_hours:.1f} ч."
        )

    def calculate_total(self):
        total = self.final_price()

        if self._on_site:
            total += 500

        return total

    def __str__(self):
        on_site_text = 'да' if self._on_site else 'нет'

        return (
            f'{super().__str__()}\n'
            f'Тип товара: услуга\n'
            f'Длительность: {self.duration_hours:.1f} ч.\n'
            f'Выезд мастера: {on_site_text}\n'
            f'Итоговая стоимость: {self.calculate_total():.2f} руб.'
        )

    def __repr__(self):
        return (
            f"Service(name='{self.name}', price={self.price}, stock={self.stock}, "
            f"category='{self.category}', discount={self.discount}, "
            f"duration_hours={self.duration_hours}, on_site={self.on_site})"
        )
    
    

class Accessory(Product):
    def __init__(
        self,
        name,
        price,
        stock,
        category,
        discount=0,
        compatibility='Универсальный',
        wireless=False
    ):
        super().__init__(name, price, stock, category, discount)
        self._compatibility = validate_text(compatibility, 'Совместимость')
        self._wireless = validate_bool(wireless, 'Беспроводной режим')

    @property
    def compatibility(self):
        return self._compatibility

    @property
    def wireless(self):
        return self._wireless

    def connect(self):
        mode = 'по Bluetooth' if self._wireless else 'по кабелю'
        return f"'{self.name}' подключен {mode}"

    def __str__(self):
        wireless_text = 'да' if self._wireless else 'нет'

        return (
            f'{super().__str__()}\n'
            f'Тип товара: аксессуар\n'
            f'Совместимость: {self.compatibility}\n'
            f'Беспроводной: {wireless_text}\n'
            f'Итоговая стоимость: {self.calculate_total():.2f} руб.'
        )

    def __repr__(self):
        return (
            f"Accessory(name='{self.name}', price={self.price}, stock={self.stock}, "
            f"category='{self.category}', discount={self.discount}, "
            f"compatibility='{self.compatibility}', wireless={self.wireless})"
        )