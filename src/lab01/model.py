from validate import (
    validate_name,
    validate_price,
    validate_stock,
    validate_category,
    validate_discount,
)


class Product:
    shop_name = 'Магазин Электроники'
    max_discount = 90

    def __init__(self, name, price, stock, category, discount=0):
        self._name = validate_name(name)
        self._price = validate_price(price)
        self._stock = validate_stock(stock)
        self._category = validate_category(category)
        self._discount = validate_discount(discount, self.max_discount)
        self._is_active = self._stock > 0

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = validate_price(value)

    @property
    def stock(self):
        return self._stock

    @property
    def category(self):
        return self._category

    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, value):
        self._discount = validate_discount(value, self.max_discount)

    @property
    def is_active(self):
        return self._is_active

    def __str__(self):
        status = 'активен' if self._is_active else 'неактивен'
        return (
            f'Товар: {self._name}\n'
            f'Категория: {self._category}\n'
            f'Обычная цена: {self._price:.2f} руб.\n'
            f'Скидка: {self._discount:.1f}%\n'
            f'Цена со скидкой: {self.final_price():.2f} руб.\n'
            f'Количество: {self._stock} шт.\n'
            f'Статус: {status}'
        )

    def __repr__(self):
        return (
            f"Product(name='{self._name}', price={self._price}, stock={self._stock}, "
            f"category='{self._category}', discount={self._discount}, is_active={self._is_active})"
        )

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False

        return (
            self._name == other._name
            and self._price == other._price
            and self._stock == other._stock
            and self._category == other._category
            and self._discount == other._discount
            and self._is_active == other._is_active
        )

    def final_price(self):
        return self._price * (1 - self._discount / 100)

    def add_stock(self, amount):
        if isinstance(amount, bool) or not isinstance(amount, int):
            raise TypeError('Добавляемое количество должно быть целым числом')

        if amount <= 0:
            raise ValueError('Добавляемое количество должно быть больше 0')

        self._stock += amount

        if self._stock > 0:
            self._is_active = True

    def buy(self, amount):
        if not self._is_active:
            raise ValueError('Нельзя купить неактивный товар')

        if isinstance(amount, bool) or not isinstance(amount, int):
            raise TypeError('Количество для покупки должно быть целым числом')

        if amount <= 0:
            raise ValueError('Количество для покупки должно быть больше 0')

        if amount > self._stock:
            raise ValueError('Нельзя купить больше товара, чем есть на складе')

        self._stock -= amount

        if self._stock == 0:
            self._is_active = False

    def deactivate(self):
        self._is_active = False


#


product1 = Product('gjhdfjgdl', 64543765446356474673, 65, 'hjfhhfjhdhjdfhjhdgdffgdjhgdjhgfej', 89)
print(product1)
product1.add_stock(10)
print(product1)