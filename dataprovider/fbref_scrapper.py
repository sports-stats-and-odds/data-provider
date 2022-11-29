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
    
        currentDateStr: str = "2022-11-25"

        # while datetime.strptime(currentDateStr, "%Y-%m-%d") < datetime.today() and False: #while currentDate < todayDate
        print(f'currentDateStr : {currentDateStr}')
        self.baseUrl += currentDateStr
        req = requests.get(self.baseUrl)
        soup = BeautifulSoup(req.content, 'html.parser')
        tables = soup.find_all('div', {"class": "table_wrapper tabbed"})
        for table in tables:
            rows = table.find_all('tr')
            rows.pop(0) #remove first row because it is the table header
            for row in rows:
                time = row.find('span', {"class": 'venuetime'}).text
                homeTeam = row.find('td', {"data-stat": 'home_team'}).find('a').text
                awayTeam = row.find('td', {"data-stat": 'away_team'}).find('a').text
                splittedScore = row.find('td', {"data-stat": 'score'}).find('a').text.split("–") #this is noty a basic dash : the charatcter is U+2013 "–" whereas a basic dash is "-"
                homeTeamScore = splittedScore[0]
                awayTeamScore = splittedScore[1]
                attendance = row.find('td', {"data-stat": 'attendance'}).text
                referee = row.find('td', {"data-stat": 'referee'}).text
                print(f"date = {currentDateStr}")
                print(f"time = {time}")
                print(f"homeTeam = {homeTeam}")
                print(f"awayTeam = {awayTeam}")
                print(f"homeTeamScore = {homeTeamScore}")
                print(f"awayTeamScore = {awayTeamScore}")
                print(f"attendance = {attendance}")
                print(f"referee = {referee}")
            # currentDateStr = getNextDateStr(currentDateStr)
            # print(tables[0].prettify())

temp = FbrefScrapper()
temp.scrap()