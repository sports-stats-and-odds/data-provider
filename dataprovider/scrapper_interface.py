from source_web_site_enum import SourceWebSite
from bs4 import BeautifulSoup
from abc import ABC

class ScrapperInterface(ABC):  

    def _get_base_url_from_website(self, website: str) -> str:
        return {
            SourceWebSite.FBREF: 'https://fbref.com/fr/matchs/',

        }[website]

    def __init__(self, website: str, ) -> None:
        self.baseUrl: str = self._get_base_url_from_website(website)
        
    def scrap(self):
        pass

    def get_link(self, link: str) -> None:
        pass
