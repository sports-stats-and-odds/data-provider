from .source_web_site_enum import SourceWebSiteEnum
from bs4 import BeautifulSoup
from abc import ABC
from connector import MySQLConnector

class ScrapperInterface(ABC):  

    def _get_base_url_from_website(self, website: str) -> str:
        return {
            SourceWebSiteEnum.FBREF: 'https://fbref.com/fr/matchs/',

        }[website]

    def __init__(self, website: str, db_connector: MySQLConnector) -> None:
        self._baseUrl: str = self._get_base_url_from_website(website)
        self._db_connector = db_connector

    def scrap(self):
        pass

    def get_link(self, link: str) -> None:
        pass
