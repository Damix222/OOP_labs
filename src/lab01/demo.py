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