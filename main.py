from dataprovider import FbrefScrapper
from connector import MySQLConnector

if __name__ == '__main__': #python -m main to run in this scope
    db_connector = MySQLConnector() #create a connection bridge with the db, the object contains all the necessary methods
    fbref_scrapper = FbrefScrapper(db_connector)
    fbref_scrapper.scrap()
    pass;
