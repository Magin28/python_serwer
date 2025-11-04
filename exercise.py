from itertools import product
import re
from typing import Optional
 
 
class Product:
    def __init__(self, name: str, price: float):
        if not re.fullmatch(r'[A-Za-z]+[0-9]+', name):
            raise ValueError(f"Niepoprawna nazwa produktu: {name}")
        self.name = name
        self.price = price

    def __eq__(self, prod: 'Product') -> bool:
        return self.name == prod.name and self.price == prod.price

    def __hash__(self):
        return hash((self.name, self.price))
 
class TooManyProductsFoundError(Exception):
    """Rzucany, gdy liczba znalezionych produktów przekracza dopuszczalny limit."""
    pass

 
 
# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania
 
class ListServer:
    n_max_returned_entries = 7
    def __init__(self, prods: list['Product']):
        self.products = prods
        pass
    def get_entries(self, n_letters):

        pattern = re.compile(rf'^[A-Za-z]{{{n_letters}}}[0-9]{{2,3}}$')
        found = [p for p in self.products if pattern.fullmatch(p.name)]
        found.sort(key=lambda p: p.price)

        if len(found) > self.n_max_returned_entries:
            raise TooManyProductsFoundError()
        return found
 
 
class MapServer:
    n_max_returned_entries = 7

    def __init__(self, prods: list['Product']):
        self.products = {p.name: p for p in prods}

    def get_entries(self, n_letters):
        pattern = re.compile(rf'^[A-Za-z]{{{n_letters}}}[0-9]{{2,3}}$')

        found = [p for p in self.products.values() if pattern.fullmatch(p.name)]
        
        found.sort(key=lambda p: p.price)

        if len(found) > self.n_max_returned_entries:
            raise TooManyProductsFoundError()
        
        return found
 
 
class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    def __init__(self, server):
        self.server = server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            entries = self.server.get_entries(n_letters)
        except TooManyProductsFoundError:
            return None
        if not entries:
            return None
        return sum(p.price for p in entries)
    