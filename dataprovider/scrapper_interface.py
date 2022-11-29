from source_web_site_enum import SourceWebSite
from bs4 import BeautifulSoup
from abc import ABC

class ScrapperInterface(ABC):  

    def _getBaseUrlFromWebsite(self, website: str) -> str:
        return {
            SourceWebSite.FBREF: 'https://fbref.com/fr/matchs/',

        }[website]

    def __init__(self, website: str, ) -> None:
        self.baseUrl: str = self._getBaseUrlFromWebsite(website)
        
    def scrap(self):
        pass

    def getLink(self, link: str) -> None:
        pass
