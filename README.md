# OOP_labs

# Лабораторная работа №1

## model.py
```python
class Product:
    shop_name = 'Магазин Электроники'
    max_discount = 90

    def __init__(self, name, price, stock, category, discount=0):
        self._name = self._validate_name(name)
        self._price = self._validate_price(price)
        self._stock = self._validate_stock(stock)
        self._category = self._validate_category(category)
        self._discount = self._validate_discount(discount)
        self._is_active = True

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

    def _validate_stock(self, value):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError('Количество должно быть целым числом')

        if value < 0:
            raise ValueError('Количество не может быть отрицательным')

        return value

    def _validate_category(self, value):
        if not isinstance(value, str):
            raise TypeError('Категория должна быть строкой')

        value = value.strip()

        if value == '':
            raise ValueError('Категория не должна быть пустой')

        return value

    def _validate_discount(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError('Скидка должна быть числом')

        value = float(value)

        if value < 0 or value > self.max_discount:
            raise ValueError(f'Скидка должна быть от 0 до {self.max_discount}')

        return value

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

    @discount.setter
    def discount(self, value):
        self._discount = self._validate_discount(value)

    @property
    def is_active(self):
        return self._is_active

    def __str__(self):
        status = 'активен' if self._is_active else 'неактивен'
        return (
            f'Товар: {self._name}\n'
            f'Категория: {self._category}\n'
            f'Обычная цена: {self._price:.2f} руб.\n'
            f'Скидка: {self._discount}%\n'
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
            and self._category == other._category
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
```
## demo.py

```python
from model import Product


def main():
    print("Создание объекта")
    product1 = Product("Ноутбук Lenovo", 80000, 5, "Электроника", 10)
    print(product1)
    print()

    print("Технический вид объекта")
    print(repr(product1))
    print()

    print("Сравнение объектов")
    product2 = Product("Ноутбук Lenovo", 80000, 3, "Электроника", 5)
    product3 = Product("Мышь Logitech", 2500, 10, "Аксессуары", 0)

    print(product1 == product2)
    print(product1 == product3)
    print()

    print("Изменение цены через setter")
    print("Старая цена:", product1.price)
    product1.price = 76000
    print("Новая цена:", product1.price)
    print("Цена со скидкой:", product1.final_price())
    print()

    print("Изменение скидки через setter")
    print("Старая скидка:", product1.discount)
    product1.discount = 15
    print("Новая скидка:", product1.discount)
    print("Цена со скидкой:", product1.final_price())
    print()

    print("Атрибут класса")
    print(Product.shop_name)
    print(product1.shop_name)
    print(Product.max_discount)
    print()

    print("Покупка товара")
    print("Остаток до покупки:", product1.stock)
    product1.buy(2)
    print("Остаток после покупки:", product1.stock)
    print()

    print("Пополнение товара")
    product1.add_stock(4)
    print("Остаток после пополнения:", product1.stock)
    print()

    print("Проверка логического состояния")
    product4 = Product("USB-кабель", 500, 1, "Аксессуары", 0)
    print(product4)
    print()

    product4.buy(1)
    print("После покупки последнего товара:")
    print(product4)
    print()

    try:
        product4.buy(1)
    except Exception as e:
        print("Ошибка:", e)
    print()

    print("Ручное изменение состояния")
    product5 = Product("Клавиатура", 3000, 7, "Аксессуары", 5)
    print(product5)
    print()

    product5.deactivate()
    print("После деактивации:")
    print(product5)
    print()

    try:
        product5.buy(1)
    except Exception as e:
        print("Ошибка:", e)
    print()

    print("Некорректное создание объекта")
    try:
        bad_product = Product("", -100, -2, "", 150)
        print(bad_product)
    except Exception as e:
        print("Ошибка:", e)
    print()

    print("Некорректная скидка")
    try:
        product1.discount = 120
    except Exception as e:
        print("Ошибка:", e)
    print()

    print("Некорректная цена")
    try:
        product1.price = -500
    except Exception as e:
        print("Ошибка:", e)
    print()

    print("Слишком большая покупка")
    try:
        product1.buy(1000)
    except Exception as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    main()
```
## Результат
![01](/images/lab01/01.png)
![02](/images/lab01/02.png)
![03](/images/lab01/03.png)