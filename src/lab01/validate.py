def validate_name(value):
    if not isinstance(value, str):
        raise TypeError('Название должно быть строкой')

    value = value.strip()

    if value == '':
        raise ValueError('Название не должно быть пустым')

    if len(value) < 2:
        raise ValueError('Название должно содержать минимум 2 символа')

    return value


def validate_price(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError('Цена должна быть числом')

    if value <= 0:
        raise ValueError('Цена должна быть больше 0')

    return float(value)


def validate_stock(value):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError('Количество должно быть целым числом')

    if value < 0:
        raise ValueError('Количество не может быть отрицательным')

    return value


def validate_category(value):
    if not isinstance(value, str):
        raise TypeError('Категория должна быть строкой')

    value = value.strip()

    if value == '':
        raise ValueError('Категория не должна быть пустой')

    return value


def validate_discount(value, max_discount):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError('Скидка должна быть числом')

    value = float(value)

    if value < 0 or value > max_discount:
        raise ValueError(f'Скидка должна быть от 0 до {max_discount}')

    return value