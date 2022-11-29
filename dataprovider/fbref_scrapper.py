from scrapper_interface import ScrapperInterface
from source_web_site_enum import SourceWebSite
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta, date

class FbrefScrapper(ScrapperInterface):
    def __init__(self) -> None:
        super().__init__(SourceWebSite.FBREF) #create soup in bases class constructor

    def scrap(self):

        def getNextDateStr(currentDate: str) -> str:
            date = datetime.strptime(currentDate, "%Y-%m-%d")
            date = date + timedelta(days=1)
            return date.strftime("%Y-%m-%d")
    
        currentDateStr: str = "2011-01-02"

        while datetime.strptime(currentDateStr, "%Y-%m-%d") < datetime.today(): #while currentDate < todayDate
            print(f'currentDateStr : {currentDateStr}')
            self.baseUrl += currentDateStr
            # req = requests.get(self.baseUrl)
            # soup = BeautifulSoup(req.content, 'html.parser')
            # tables = soup.find_all('div', {"class": "table_wrapper tabbed"})
            currentDateStr = getNextDateStr(currentDateStr)
        # print(tables[0].prettify())

temp = FbrefScrapper()
temp.scrap()