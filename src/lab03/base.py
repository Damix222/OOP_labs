from src.lib.model import Product as BaseProduct


class Product(BaseProduct):
    """Базовый класс ЛР-3 с общим интерфейсом расчёта итоговой стоимости."""

    def calculate_total(self):
        return self.final_price()