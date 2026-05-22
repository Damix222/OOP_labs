from __future__ import annotations

import json
from pathlib import Path
from typing import Any, TypeAlias

from src.lab03.base import Product
from src.lab04.models import Accessory, DigitalProduct, Service


ProductItem: TypeAlias = Product | DigitalProduct | Service | Accessory


def _product_to_dict(item: ProductItem, added_at: str | None = None) -> dict[str, Any]:
    """Преобразовать объект товара в словарь для JSON."""
    base_data: dict[str, Any] = {
        'name': item.name,
        'price': item.price,
        'stock': item.stock,
        'category': item.category,
        'discount': item.discount,
        'added_at': added_at,
    }

    if isinstance(item, DigitalProduct):
        base_data.update(
            {
                'type': 'digital',
                'file_size_mb': item.file_size_mb,
                'license_type': item.license_type,
            }
        )
        return base_data

    if isinstance(item, Service):
        base_data.update(
            {
                'type': 'service',
                'duration_hours': item.duration_hours,
                'on_site': item.on_site,
            }
        )
        return base_data

    if isinstance(item, Accessory):
        base_data.update(
            {
                'type': 'accessory',
                'compatibility': item.compatibility,
                'wireless': item.wireless,
            }
        )
        return base_data

    if isinstance(item, Product):
        base_data['type'] = 'product'
        return base_data

    raise TypeError('Неизвестный тип объекта')


def _dict_to_product(data: dict[str, Any]) -> ProductItem:
    """Создать объект товара из словаря."""
    product_type = data.get('type')

    if product_type == 'product':
        return Product(
            name=data['name'],
            price=data['price'],
            stock=data['stock'],
            category=data['category'],
            discount=data.get('discount', 0),
        )

    if product_type == 'digital':
        return DigitalProduct(
            name=data['name'],
            price=data['price'],
            stock=data['stock'],
            category=data['category'],
            discount=data.get('discount', 0),
            file_size_mb=data.get('file_size_mb', 1),
            license_type=data.get('license_type', 'Стандартная'),
        )

    if product_type == 'service':
        return Service(
            name=data['name'],
            price=data['price'],
            stock=data['stock'],
            category=data['category'],
            discount=data.get('discount', 0),
            duration_hours=data.get('duration_hours', 1),
            on_site=data.get('on_site', False),
        )

    if product_type == 'accessory':
        return Accessory(
            name=data['name'],
            price=data['price'],
            stock=data['stock'],
            category=data['category'],
            discount=data.get('discount', 0),
            compatibility=data.get('compatibility', 'Универсальный'),
            wireless=data.get('wireless', False),
        )

    raise ValueError(f'Неизвестный тип товара: {product_type}')


def save(
    items: list[ProductItem],
    filepath: str,
    added_at: dict[str, str] | None = None,
) -> None:
    """Сохранить список товаров в JSON-файл."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    metadata = added_at or {}
    data = [
        _product_to_dict(item, metadata.get(item.name))
        for item in items
    ]

    with path.open('w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load(filepath: str) -> tuple[list[ProductItem], dict[str, str]]:
    """Загрузить товары из JSON-файла."""
    path = Path(filepath)

    if not path.exists():
        return [], {}

    with path.open('r', encoding='utf-8') as file:
        raw_data = json.load(file)

    if not isinstance(raw_data, list):
        raise ValueError('Файл должен содержать список объектов')

    items: list[ProductItem] = []
    added_at: dict[str, str] = {}

    for item_data in raw_data:
        if not isinstance(item_data, dict):
            raise ValueError('Каждый элемент JSON должен быть объектом')

        product = _dict_to_product(item_data)
        items.append(product)

        date_value = item_data.get('added_at')
        if isinstance(date_value, str):
            added_at[product.name] = date_value

    return items, added_at