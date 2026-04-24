from src.lib.normalize import normalize
from src.lab03.models import (
    DigitalProduct as BaseDigitalProduct,
    Service as BaseService,
    Accessory as BaseAccessory,
)
from src.lab04.interfaces import Printable, Actionable, Sortable


class DigitalProduct(BaseDigitalProduct, Printable, Actionable, Sortable):
    def to_string(self):
        return (
            f'[Цифровой товар] {self.name} | '
            f'Категория: {self.category} | '
            f'Лицензия: {self.license_type} | '
            f'Размер файла: {self.file_size_mb:.1f} МБ | '
            f'Итоговая цена: {self.calculate_total():.2f} руб.'
        )

    def do_action(self):
        return self.activate_license()

    def sort_key(self):
        return (
            normalize(self.category),
            normalize(self.name),
            self.file_size_mb
        )


class Service(BaseService, Printable, Actionable, Sortable):
    def to_string(self):
        on_site_text = 'да' if self.on_site else 'нет'

        return (
            f'[Услуга] {self.name} | '
            f'Категория: {self.category} | '
            f'Длительность: {self.duration_hours:.1f} ч. | '
            f'Выезд мастера: {on_site_text} | '
            f'Итоговая цена: {self.calculate_total():.2f} руб.'
        )

    def do_action(self):
        return self.book_service()

    def sort_key(self):
        return (
            normalize(self.category),
            normalize(self.name),
            self.duration_hours
        )


class Accessory(BaseAccessory, Printable, Actionable, Sortable):
    def to_string(self):
        wireless_text = 'да' if self.wireless else 'нет'

        return (
            f'[Аксессуар] {self.name} | '
            f'Категория: {self.category} | '
            f'Совместимость: {self.compatibility} | '
            f'Беспроводной: {wireless_text} | '
            f'Итоговая цена: {self.calculate_total():.2f} руб.'
        )

    def do_action(self):
        return self.connect()

    def sort_key(self):
        wireless_order = 0 if self.wireless else 1
        return (
            normalize(self.category),
            normalize(self.name),
            wireless_order
        )