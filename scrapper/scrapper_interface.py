from .source_web_site_enum import SourceWebSiteEnum
from bs4 import BeautifulSoup
from abc import ABC
from connector import MySQLConnector
import logger
import os

class ScrapperInterface(ABC):  

    def _get_base_url_from_website(self, website: str) -> str:
        return {
            SourceWebSiteEnum.FBREF: 'https://fbref.com/fr/matchs/',

        }[website]

    def __init__(self, website: str, db_connector: MySQLConnector) -> None:
        self._baseUrl: str = self._get_base_url_from_website(website)
        self._db_connector = db_connector
        self._logger = logger.get_logger(os.path.dirname(os.path.abspath(__file__)) + "/logs/")


    def scrap(self):
        pass

    def get_link(self, link: str) -> None:
        pass
