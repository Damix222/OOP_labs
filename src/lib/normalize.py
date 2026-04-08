def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    if not isinstance(text, str):
        raise TypeError('Значение должно быть строкой')

    if casefold:
        text = text.casefold()

    if yo2e:
        text = text.replace('ё', 'е').replace('Ё', 'Е')

    text = text.replace('\t', ' ').replace('\r', ' ').replace('\n', ' ')
    text = ' '.join(text.split())
    text = text.strip()

    return text