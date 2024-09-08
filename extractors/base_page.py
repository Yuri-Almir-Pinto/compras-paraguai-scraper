import requests
from extractors.standard import BASE_URL, extract_price, ScrapingException
from bs4 import BeautifulSoup, Tag

from extractors.product_list import ProductsList

class BasePage:
    def __init__(self, base_url: str, session: requests.Session = None):
        self.base_url = base_url
        
        html = session.get(self.base_url).text if session is not None else requests.get(self.base_url).text
        
        self.base_html = BeautifulSoup(html, 'html.parser')
        self.product_list = self.get_product_list()
        self.last_page = self.get_last_page()
        self.all_pages_url = self.get_all_pages_urls()
        
    def get_product_list(self) -> ProductsList:
        resultados_busca = self.base_html.select_one(".resultados-busca")
        if resultados_busca is None: raise ScrapingException("Product div not found")
        
        return ProductsList(resultados_busca)
    
    def get_last_page(self) -> int:
        pagination_elements = self.base_html.select(".pagination .page")
        if len(pagination_elements) == 0: raise ScrapingException("Pagination not found")
        
        last_page_element = pagination_elements[-1]
        if last_page_element is None: raise ScrapingException("Last page not found")
        
        return int(last_page_element.text)
    
    def get_all_pages_urls(self):
        page_urls = []
        for page in range(1, self.last_page + 1):
            page_url = f"{self.base_url}&page={page}" if "?" in self.base_url else f"{self.base_url}?page={page}"
            page_urls.append(page_url)
            
        return page_urls
