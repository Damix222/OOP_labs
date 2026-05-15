from src.lib.model import Product as BaseProduct


class Product(BaseProduct):
    """Базовый класс ЛР-3 с общим интерфейсом расчёта итоговой стоимости."""

    def calculate_total(self) -> float:
        return self.final_price()

    def display(self) -> str:
        return str(self)

    def score(self) -> float:
        return self.calculate_total()