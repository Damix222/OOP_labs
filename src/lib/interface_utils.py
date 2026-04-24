from src.lab04.interfaces import Printable, Actionable, Sortable


def print_all(items: list[Printable]):
    for item in items:
        print(item.to_string())


def run_all_actions(items: list[Actionable]):
    for item in items:
        print(item.do_action())


def sort_items(items: list[Sortable], reverse=False):
    return sorted(items, key=lambda item: item.sort_key(), reverse=reverse)