import requests
from extractors.standard import BASE_URL, InvalidElementException, extract_price, ScrapingException
from bs4 import BeautifulSoup, Tag
from extractors.product import Product

class ProductsList:
    def __init__(self, product_list_element: Tag):
        if 'resultados-busca' not in product_list_element['class']:
            raise InvalidElementException("Element is not a product list")
        
        # self.product_list_element = product_list_element
        product_elements = product_list_element.select(".promocao-produtos-item")
        if len(product_elements) == 0: raise ScrapingException("Product list element does not have any products")
        
        self.products = [Product(product_element) for product_element in product_elements]
    
    def __getitem__(self, index) -> Product:
        return self.products[index]
    
    def __repr__(self) -> str:
        return f"ProductsList({self.products})"
        