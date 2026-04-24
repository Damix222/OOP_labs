from abc import ABC, abstractmethod


class Printable(ABC):
    @abstractmethod
    def to_string(self):
        pass


class Actionable(ABC):
    @abstractmethod
    def do_action(self):
        pass


class Sortable(ABC):
    @abstractmethod
    def sort_key(self):
        pass