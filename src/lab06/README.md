# ЛР-6 — Generics и typing

## Цель работы

Освоить аннотации типов, generic-классы через `TypeVar` и `Generic`, а также структурную типизацию через `Protocol`.

---

## Что реализовано

В ЛР-6 добавлены:

- аннотации типов в классы;
- generic-контейнер `TypedCollection`;
- методы `find()`, `filter()`, `map()`;
- протоколы `Displayable` и `Scorable`.

Контейнер находится в файле `container.py`.

```python
T = TypeVar('T')

class TypedCollection(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []
```

Пример использования:

```python
digital_collection: TypedCollection[DigitalProduct] = TypedCollection(DigitalProduct)
```

Для сравнения названий и категорий используется `normalize()`.

---

## Методы коллекции

В `TypedCollection` перенесены методы из ЛР-2:

- `add()`;
- `remove()`;
- `get_all()`;
- `find_by_name()`;
- `find_by_category()`;
- `sort_by_name()`;
- `sort_by_price()`;
- `get_active()`;
- `get_available()`;
- `get_expensive()`.

Также добавлены методы:

```python
def find(self, predicate: Callable[[T], bool]) -> T | None:
    ...

def filter(self, predicate: Callable[[T], bool]) -> list[T]:
    ...

def map(self, transform: Callable[[T], R]) -> list[R]:
    ...
```

`map()` использует второй `TypeVar` — `R`, потому что результат может быть другого типа:

```python
names: list[str] = digital_collection.map(lambda item: item.name)
totals: list[float] = digital_collection.map(lambda item: item.calculate_total())
```

---

## Protocol

Реализованы два протокола:

```python
class Displayable(Protocol):
    def display(self) -> str:
        ...

class Scorable(Protocol):
    def score(self) -> float:
        ...
```

`DigitalProduct`, `Service` и `Accessory` подходят под эти протоколы без явного наследования, если у них есть методы `display()` и `score()`.

---

## Демонстрация

### Сценарий 1. Типизированная коллекция DigitalProduct ✅

Создаётся `TypedCollection[DigitalProduct]`, добавляются цифровые товары.

![01](/images/lab06/01.png)

---

### Сценарий 2. `get_all()` и проверка типа ✅

Выводятся все элементы. Затем показана ошибка при добавлении `Service` в коллекцию `DigitalProduct`.

![02](/images/lab06/02.png)

---

### Сценарий 3. `find()` ✅

Один товар найден, второй поиск возвращает `None`.

![03](/images/lab06/03.png)

---

### Сценарий 4. `filter()` ✅

Показана фильтрация товаров по наличию и цене.

![04](/images/lab06/04.png)

---

### Сценарий 5. `map()` ✅

Коллекция преобразуется в `list[str]` и `list[float]`.

![05](/images/lab06/05.png)

---

### Сценарий 6. Protocol `Displayable` ✅

Объекты разных классов добавляются в `TypedCollection[Displayable]`, затем вызывается `display()`.

![06](/images/lab06/06.png)
![06.1](/images/lab06/06.1.png)
---

### Сценарий 7. Protocol `Scorable` ✅

Объекты разных классов добавляются в `TypedCollection[Scorable]`, затем вызывается `score()`.

![07](/images/lab06/07.png)

---

### Сценарий 8. Один контейнер с разными ограничениями ✅

`TypedCollection` используется с `Displayable` и `Scorable`.

![08](/images/lab06/08.png)


---

## Вывод

В работе были изучены `typing`, `Generic`, `TypeVar`, `Callable` и `Protocol`.

Реализован типизированный контейнер `TypedCollection`, который хранит объекты заданного типа и поддерживает поиск, фильтрацию и преобразование данных.
