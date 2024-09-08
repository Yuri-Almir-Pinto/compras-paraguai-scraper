import requests
from extractors.standard import BASE_URL, extract_price, ScrapingException
from bs4 import BeautifulSoup, Tag


class Product:
    def __init__(self, product_element: Tag):
        self.product_element = product_element
        self.href = self.get_product_href()
        self.page_url = BASE_URL + self.href
        self.name = self.get_product_name()
        (price_reals, price_dollars) = self.get_product_price()
        self.price_reals = price_reals
        self.price_dollars = price_dollars
        self.details = {}
        
    def __repr__(self):
        return f"Product(name='{self.name}', price_reals={self.price_reals}, price_dollars={self.price_dollars}, href='{self.href}')"
    
    def get_product_name(self) -> str:
        product_name = self.product_element.select_one(".promocao-item-nome a")
        if product_name is None: raise ScrapingException("Product name not found")
        
        return product_name.text
    
    def get_product_price(self) -> tuple[float, float]:
        product_price_element = self.product_element.select_one(".container-price .price-model")
        
        if product_price_element is not None: 
            dolar_price_element = product_price_element.select_one("span")
            reals_price_element = product_price_element.select_one(".promocao-item-preco-text")
            if dolar_price_element is None or reals_price_element is None: 
                raise ScrapingException(f"Product price (Standard) not found on: {self.page_url}")
            
            return (extract_price(reals_price_element.text),
                extract_price(dolar_price_element.text))
            
        else:
            product_price_element = self.product_element.select_one(".promocao-item-preco-oferta")
            if product_price_element is None: raise ScrapingException(f"Product price not found on: {self.page_url}")
            dolar_price_element = product_price_element.select_one(".preco-dolar")
            reals_price_element = product_price_element.select_one(".preco-produto")
            if dolar_price_element is None or reals_price_element is None: 
                raise ScrapingException(f"Product price (Offer) not found on: {self.page_url}")
            
            return (extract_price(reals_price_element.text),
                extract_price(dolar_price_element.text))
        
        
    def get_product_href(self) -> str:
        product_name = self.product_element.select_one(".promocao-item-nome a")
        if product_name is None: raise ScrapingException("Product name not found")
        
        return product_name.get('href')
    
    def get_details(self, session: requests.Session = None) -> dict:
        html = session.get(self.page_url).text if session is not None else requests.get(self.page_url).text
        
        product_page = BeautifulSoup(html, 'html.parser')
        table_rows = product_page.select(".table-details tr")
        if table_rows is None: raise ScrapingException("Table not found")
        self.details = {}
        
        for row in table_rows:
            [tr_1, tr_2] = row.select("td")
            
            key = tr_1.text.strip()
            value = tr_2.text.strip()
            self.details[key] = value
        
        return self.details
    