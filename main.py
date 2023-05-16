import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from logging.config import fileConfig
from pathlib import Path
from unicodedata import normalize
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
from sqlalchemy import URL
from datetime import date
from email import encoders
# from pandasql import sqldf

import pandas as pd
# from pandas import DataFrame as df
from sqlalchemy import text

# Set working directory
app_folder = Path(__file__).parent
os.chdir(app_folder)

# Create logs folder if needed
Path('logs/').mkdir(exist_ok=True)

# Configure logging
logging_config_path = app_folder / 'logging_config.ini'
fileConfig(logging_config_path, disable_existing_loggers=False)
log = logging.getLogger()

def main():
    import sqldf

    conn_str = 'DRIVER={SQL Server};Server=DESKTOP-UB80N6S;Database=Staging;Trusted_Connection=True;'
    # cnxn = pyodbc.connect(conn_str)
    connection_url = URL.create(
        "mssql+pyodbc", 
        query={"odbc_connect": conn_str}
    )
    staging_engine = create_engine(connection_url, use_setinputsizes=False)

    conn_str = 'DRIVER={SQL Server};Server=DESKTOP-UB80N6S;Database=GG;Trusted_Connection=True;'
    # cnxn = pyodbc.connect(conn_str)
    connection_url = URL.create(
        "mssql+pyodbc", 
        query={"odbc_connect": conn_str}
    )
    gg_engine = create_engine(connection_url, use_setinputsizes=False)
    # engine = create_engine(conn_str)

    url = 'http://ratingupdate.info/player/2EC3DA77B57ADAA/RA'
    browser = webdriver.Chrome()
    browser.implicitly_wait(10)
    browser.get(url)
    browser.find_element(By.XPATH, """//*[@id="history"]/div/table""")
    html = browser.page_source

    table_MN = pd.read_html(html)
    print(len(table_MN))

    df = table_MN[0]
    df = df.drop('Floor', axis='columns')
    df['wins'] = df['Result'].str[:2]
    df['wins'].fillna(0)
    # print(df)
    df['wins'] = df['wins'].astype(int)
    df['losses'] = df['Result'].str[-2:]
    df['losses'].fillna(0)
    df['losses'] = df['losses'].astype(int)

    cols = {
    'Date':'data_datetime',
    	'Rating':'my_rating',
    	'Opponent':'opp_name',
    	'Character':'opp_char',
    	'Rating.1':'opp_rating',
	    'Odds':'win_odds', 
        'wins':'wins',
        'losses':'losses',
        'Rating change':'rating_change' }
    df.rename(columns = cols, inplace = True)

    today = date.today().strftime("%Y-%m-%d")
    print("Today's date:", today)
    q = f"SELECT * FROM df WHERE [data_datetime] like '{today}%'"
    # q = f"SELECT * FROM df WHERE [data_datetime] like '2023-03-19%'"
    scope = locals()
    df = sqldf.run(q, scope)
    df = df.drop('index', axis='columns')
    print(df)

    if df.empty == False:
        df.to_sql('Games', con=staging_engine, schema='dbo', if_exists='append', index=False)
        print('Rows uploaded')

    staging_engine.dispose()
    gg_engine.dispose()
    log.debug('Exiting main()')

if __name__ == '__main__':
    try:
        main()
    except:
        log.exception('Exception caught at top level')
        raise