from .scrapper_interface import ScrapperInterface
from .source_web_site_enum import SourceWebSiteEnum
from bs4 import BeautifulSoup
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
    
        currentDateStr: str = "1888-01-01"

        while datetime.strptime(currentDateStr, "%Y-%m-%d") < datetime.today(): #while currentDate < todayDate
            self._logger.info("------------------------------------")
            self._logger.info(f"Adding data for {currentDateStr}")
            soup = self._get_url_soup(self._baseUrl + currentDateStr)
            if soup == None: continue
            tables = soup.find_all('div', {"class": "table_wrapper tabbed"})
            for table in tables:
                contest = table.find('span', {"class": 'section_anchor'}).text[:-2] #remove last 2 characters, which are '">'
                rows = table.find_all('tr')
                rows.pop(0) #remove first row because it is the table header
                for row in rows:
                    try:
                        hour = row.find('span', {"class": 'venuetime'}).text
                        homeTeam = row.find('td', {"data-stat": 'home_team'}).find('a').text
                        awayTeam = row.find('td', {"data-stat": 'away_team'}).find('a').text
                        splittedScore = row.find('td', {"data-stat": 'score'}).find('a').text.split("–") #this is noty a basic dash : the charatcter is U+2013 "–" whereas a basic dash is "-"
                        homeTeamScore = splittedScore[0]
                        awayTeamScore = splittedScore[1]
                        round = row.find('th', {"data-stat": 'round'}).find('a').text
                        gameweek_td = row.find('td', {"data-stat": 'gameweek'})
                        gameweek = gameweek_td.text if gameweek_td != None else None
                        grandstand = row.find('td', {"data-stat": 'venue'}).text
                        attendance = row.find('td', {"data-stat": 'attendance'}).text
                        referee = row.find('td', {"data-stat": 'referee'}).text
                        self._db_connector.insert(
                            Table.FOOTBALL_MATCH,
                            {
                                "id": currentDateStr + '-' + homeTeam + '-' + awayTeam + '-' + contest.lower(),
                                "date": currentDateStr,
                                "hour": hour,
                                "homeTeam": homeTeam,
                                "awayTeam": awayTeam,
                                "homeTeamScore": homeTeamScore,
                                "awayTeamScore": awayTeamScore,
                                "contest": contest,
                                "round": round,
                                "gameweek": gameweek if gameweek != '' else None,
                                "grandstand": grandstand,
                                "attendance": attendance.replace(',', '') if attendance != '' else None,
                                "referee": referee,
                            }
                        )
                    except Exception as error:
                        self._logger.error(repr(error))
            currentDateStr = getNextDateStr(currentDateStr)
            sleep(2)

