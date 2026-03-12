class Product:
    def __init__(self, name, price, stock, category, discount):
        self._name = self._validate_name(name)
        self._price = self._validate_price(price)

        if not isinstance(stock, int):
            raise TypeError('Количество должно быть целым числом')
        if stock < 0:
            raise ValueError('Количество не может быть отрицательным')

        if not isinstance(category, str):
            raise TypeError('Категория должна быть строкой')
        if category.strip() == '':
            raise ValueError('Категория не должна быть пустой')

        if not isinstance(discount, (int, float)):
            raise TypeError('Скидка должна быть числом')
        if discount < 0 or discount > 90:
            raise ValueError('Скидка должна быть от 0 до 90')

        self._stock = stock
        self._category = category
        self._discount = discount

    def _validate_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Название должно быть строкой')

        value = value.strip()

        if value == '':
            raise ValueError('Название не должно быть пустым')

        if len(value) < 2:
            raise ValueError('Название должно содержать минимум 2 символа')

        return value

    def _validate_price(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError('Цена должна быть числом')
        if value <= 0:
            raise ValueError('Цена должна быть больше 0')
        return float(value)

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = self._validate_price(value)

    @property
    def stock(self):
        return self._stock

    @property
    def category(self):
        return self._category

    @property
    def discount(self):
        return self._discount