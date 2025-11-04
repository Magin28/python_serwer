from abc import ABC, abstractmethod
import re
from typing import List, Optional


class Product:
    def __init__(self, name: str, price: float):
        if not re.fullmatch(r'[A-Za-z]+[0-9]+', name):
            raise ValueError(f"Niepoprawna nazwa produktu: {name}")
        self.name = name
        self.price = price

    def __eq__(self, prod: 'Product') -> bool:
        if not isinstance(prod, Product):
            return False
        return self.name == prod.name and self.price == prod.price

    def __hash__(self):
        return hash((self.name, self.price))


class TooManyProductsFoundError(Exception):
    """Rzucany, gdy liczba znalezionych produktów przekracza dopuszczalny limit."""
    pass


class Server(ABC):
    n_max_returned_entries = 7

    def __init__(self, products: List[Product]):
        self.products = products

    def validate_n_letters(self, n_letters: Optional[int]) -> int:
        if not isinstance(n_letters, int) or n_letters < 1:
            raise ValueError("Liczba liter musi być liczbą całkowitą większą lub równą 1.")
        return n_letters
    
    @abstractmethod
    def get_entries(self, n_letters: Optional[int]) -> List[Product]:
        """Metoda, która musi być zaimplementowana w klasie potomnej."""
        pass


class ListServer(Server):
    def __init__(self, products: List[Product]):
        super().__init__(products)

    def get_entries(self, n_letters: Optional[int]) -> List[Product]:
        n_letters = self.validate_n_letters(n_letters)
        pattern = re.compile(rf'^[A-Za-z]{{{n_letters}}}[0-9]{{2,3}}$')
        found = [p for p in self.products if pattern.fullmatch(p.name)]
        found.sort(key=lambda p: p.price)

        if len(found) > self.n_max_returned_entries:
            raise TooManyProductsFoundError("Zbyt wiele produktów spełnia kryteria.")
        
        return found


class MapServer(Server):
    def __init__(self, products: List[Product]):
        super().__init__(products)
        # Mapa produktów (słownik z kluczem będącym nazwą produktu)
        self.products = {p.name: p for p in self.products}

    def get_entries(self, n_letters: Optional[int]) -> List[Product]:
        n_letters = self.validate_n_letters(n_letters)
        pattern = re.compile(rf'^[A-Za-z]{{{n_letters}}}[0-9]{{2,3}}$')

        found = [p for p in self.products.values() if pattern.fullmatch(p.name)]
        found.sort(key=lambda p: p.price)

        if len(found) > self.n_max_returned_entries:
            raise TooManyProductsFoundError("Zbyt wiele produktów spełnia kryteria.")
        
        return found


class Client:
    def __init__(self, server: Server):
        self.server = server

    def get_total_price(self, n_letters: Optional[int] = None) -> Optional[float]:
        try:
            entries = self.server.get_entries(n_letters)
        except TooManyProductsFoundError:
            return None
        except ValueError:
            return None
        return sum(p.price for p in entries) if entries else None
