from .source_web_site_enum import SourceWebSiteEnum
from bs4 import BeautifulSoup
from abc import ABC
from connector import MySQLConnector
import logger
import os
import requests
from typing import Optional

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

    def _get_url_soup(self, url: str) -> Optional[BeautifulSoup]:
        try:
            req = requests.get(url)
            soup = BeautifulSoup(req.content, 'html.parser')
            return soup
        except Exception as error:
            self._logger.error(f'An error occured while fetching this url : {url}\nError : {repr(error)}')
        return None