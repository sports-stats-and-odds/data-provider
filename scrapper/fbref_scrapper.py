from .scrapper_interface import ScrapperInterface
from .source_web_site_enum import SourceWebSiteEnum
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta, date
from time import sleep
from connector import MySQLConnector, Table

class FbrefScrapper(ScrapperInterface):
    def __init__(self, db_connector: MySQLConnector) -> None:
        super().__init__(SourceWebSiteEnum.FBREF, db_connector) #create soup in base class constructor

    def scrap(self):

        def getNextDateStr(currentDate: str) -> str:
            date = datetime.strptime(currentDate, "%Y-%m-%d")
            date = date + timedelta(days=1)
            return date.strftime("%Y-%m-%d")
    
        currentDateStr: str = "1888-01-01" #1888-01-01

        while datetime.strptime(currentDateStr, "%Y-%m-%d") < datetime.today(): #while currentDate < todayDate
            self._logger.info("-----------------------------------------------------")
            self._logger.info(f"Adding data for {currentDateStr}")
            url = self._baseUrl + currentDateStr
            print(f"url = {url}")
            req = requests.get(url)
            soup = BeautifulSoup(req.content, 'html.parser')
            tables = soup.find_all('div', {"class": "table_wrapper tabbed"})

            for table in tables:
                rows = table.find_all('tr')
                rows.pop(0) #remove first row because it is the table header
                for row in rows:
                    hour = row.find('span', {"class": 'venuetime'}).text
                    homeTeam = row.find('td', {"data-stat": 'home_team'}).find('a').text
                    awayTeam = row.find('td', {"data-stat": 'away_team'}).find('a').text
                    splittedScore = row.find('td', {"data-stat": 'score'}).find('a').text.split("–") #this is noty a basic dash : the charatcter is U+2013 "–" whereas a basic dash is "-"
                    homeTeamScore = splittedScore[0]
                    awayTeamScore = splittedScore[1]
                    attendance = row.find('td', {"data-stat": 'attendance'}).text
                    referee = row.find('td', {"data-stat": 'referee'}).text
                    self._db_connector.insert(
                        Table.FOOTBALL_MATCH,
                        {
                            "id": currentDateStr + '-' + homeTeam + '-' + awayTeam,
                            "date": currentDateStr,
                            "hour": hour,
                            "homeTeam": homeTeam,
                            "awayTeam": awayTeam,
                            "homeTeamScore": homeTeamScore,
                            "awayTeamScore": awayTeamScore,
                            "attendance": attendance.replace(',', '') if attendance != '' else None,
                            "referee": referee,
                        }
                    )
            currentDateStr = getNextDateStr(currentDateStr)
            print(f"currentDateStr = {currentDateStr}")
            sleep(2)

