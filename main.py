from dataprovider import FbrefScrapper
from connector import MySQLConnector
import logger
import os

if __name__ == '__main__': #python -m main to run in this scope
    logger = logger.get_logger(os.path.dirname(os.path.abspath(__file__)) + "/logs/")
    logger.info("bonjour ?")
    db_connector = MySQLConnector() #create a connection bridge with the db, the object contains all the necessary methods
    db_connector.create_tables_if_not_exists()
    
    fbref_scrapper = FbrefScrapper(db_connector)
    fbref_scrapper.scrap()
    pass;
