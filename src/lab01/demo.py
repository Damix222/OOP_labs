from model import Product


def main():
    print("Создание объекта")
    product1 = Product("Ноутбук Lenovo", 80000, 5, "Электроника", 10)
    print(product1)
    print()

    print("Сравнение объектов")
    product2 = Product("Ноутбук Lenovo", 80000, 3, "Электроника", 5)
    print(product1 == product2)
    print()

    print("Изменение цены и скидки")
    print("Старая цена:", product1.price)
    product1.price = 76000
    product1.discount = 15
    print("Новая цена:", product1.price)
    print("Новая скидка:", product1.discount)
    print("Цена со скидкой:", product1.final_price())
    print()

    print("Атрибут класса")
    print(Product.shop_name)
    print(product1.shop_name)
    print()

    print("Покупка товара")
    print("Остаток до покупки:", product1.stock)
    product1.buy(2)
    print("Остаток после покупки:", product1.stock)
    print()

    print("Изменение состояния")
    product3 = Product("USB-кабель", 500, 1, "Аксессуары", 0)
    print(product3)
    print()

    product3.deactivate()
    print("После деактивации:")
    print(product3)
    print()

    try:
        product3.buy(1)
    except Exception as e:
        print("Ошибка:", e)
    print()

    print("Проверка валидации")
    try:
        bad_product = Product("", -100, -2, "", 150)
        print(bad_product)
    except Exception as e:
        print("Ошибка:", e)

    try:
        product1.price = -500
    except Exception as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    main()