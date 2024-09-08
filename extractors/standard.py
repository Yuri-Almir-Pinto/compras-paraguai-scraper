import re

BASE_URL: str = "https://www.comprasparaguai.com.br"

def extract_price(price_text):
    price_numbers = re.findall(r'\d+[\.,]?\d*', price_text)
    price = float(price_numbers[0].replace(',', '.'))
    return price
    
class ScrapingException(Exception):
    def __init__(self, message):
        super().__init__(message)
        
class InvalidElementException(Exception):
    def __init__(self, message):
        super().__init__(message)