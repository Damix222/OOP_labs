class ItemNotFoundError(Exception):
    """Объект не найден в коллекции."""


class DuplicateItemError(Exception):
    """Объект с таким названием уже существует."""


class StorageError(Exception):
    """Ошибка при сохранении или загрузке данных."""
