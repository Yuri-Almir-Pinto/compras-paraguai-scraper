import requests
from extractors.standard import BASE_URL, extract_price, ScrapingException
from bs4 import BeautifulSoup, Tag
import concurrent.futures

from extractors.base_page import BasePage

class BasePageList:
    def __init__(self, first_url: str):
        first_page = BasePage(first_url)
        self.base_pages: list[BasePage] = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            with requests.Session() as session:
                futures = [executor.submit(BasePage, url, session) for url in first_page.all_pages_url]
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    self.base_pages.append(result)
                
    def __getitem__(self, index) -> BasePage:
        return self.base_pages[index]
    
    def set_all_product_details(self):
        import concurrent.futures
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            with requests.Session() as session:
                for page in self.base_pages:
                    [executor.submit(product.get_details, session) for product in page.product_list.products]
        
