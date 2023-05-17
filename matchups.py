import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
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
# from pandas import DataFrame as df
from sqlalchemy import text

conn_str = 'DRIVER={SQL Server};Server=DESKTOP-UB80N6S;Database=GG;Trusted_Connection=True;'
    # cnxn = pyodbc.connect(conn_str)
connection_url = URL.create(
    "mssql+pyodbc", 
    query={"odbc_connect": conn_str}
)
gg_engine = create_engine(connection_url, use_setinputsizes=False)

q = """
SELECT 
	opp_char as Character
	, round(SUM(cast(wins as float))/SUM(wins + losses) * 100, 2) as [Win %]
	, SUM(cast(SUBSTRING(opp_rating, 1, 4) as int)) / count(1) as [Avg Rating]
	, SUM(wins + losses) as Volume
  FROM [GG].[dbo].[Games]
  Group By opp_char
  Order By [Win %]
"""

df = pd.read_sql(q, gg_engine.raw_connection())

tmp = df.to_html(index=None, border=0)
with open(r'C:\\Repos\\GG_Data\\email_body.html', 'r') as file:
    email_body = file.read()

email_body = email_body.replace('{{table}}', str(tmp))

char_img = {
    'Ramlethal': """<img src="https://www.dustloop.com/wiki/images/thumb/f/fb/GGST_Ramlethal_Valentine_Icon.png/85px-GGST_Ramlethal_Valentine_Icon.png" alt="Ramlethal" />""",
    'Testament': """<img src="https://www.dustloop.com/wiki/images/thumb/3/32/GGST_Testament_Icon.png/85px-GGST_Testament_Icon.png" alt="Testament" />""",
    "Jack-O'": """<img src="https://www.dustloop.com/wiki/images/thumb/6/65/GGST_Jack-O%27_Icon.png/85px-GGST_Jack-O%27_Icon.png" alt="Jack-O'" />""",
    'Nagoriyuki': """<img src="https://www.dustloop.com/wiki/images/thumb/2/2c/GGST_Nagoriyuki_Icon.png/85px-GGST_Nagoriyuki_Icon.png" alt="Nagoriyuki" />""",
    'Millia': """<img src="https://www.dustloop.com/wiki/images/thumb/d/d8/GGST_Millia_Rage_Icon.png/85px-GGST_Millia_Rage_Icon.png" alt="Millia" />""",
    'Chipp': """<img src="https://www.dustloop.com/wiki/images/thumb/9/94/GGST_Chipp_Zanuff_Icon.png/85px-GGST_Chipp_Zanuff_Icon.png" alt="Chipp" />""",
    'Sol': """<img src="https://www.dustloop.com/wiki/images/thumb/7/75/GGST_Sol_Badguy_Icon.png/85px-GGST_Sol_Badguy_Icon.png" alt="Sol" />""",
    'Ky': """<img src="https://www.dustloop.com/wiki/images/thumb/d/d8/GGST_Ky_Kiske_Icon.png/85px-GGST_Ky_Kiske_Icon.png" alt="Ky" />""",
    'May': """<img src="https://www.dustloop.com/wiki/images/thumb/5/51/GGST_May_Icon.png/85px-GGST_May_Icon.png" alt="May" />""",
    'Zato-1': """<img src="https://www.dustloop.com/wiki/images/thumb/5/51/GGST_Zato-1_Icon.png/85px-GGST_Zato-1_Icon.png" alt="Zato-1" />""",
    'I-No': """<img src="https://www.dustloop.com/wiki/images/thumb/9/94/GGST_I-No_Icon.png/85px-GGST_I-No_Icon.png" alt="I-No" />""",
    'Happy Chaos': """<img src="https://www.dustloop.com/wiki/images/thumb/7/78/GGST_Happy_Chaos_Icon.png/85px-GGST_Happy_Chaos_Icon.png" alt="Happy Chaos" />""",
    'Bedman?': """<img src="https://www.dustloop.com/wiki/images/thumb/e/ec/GGST_Bedman_Icon.png/85px-GGST_Bedman_Icon.png" alt="Bedman?" />""",
    'Sin': """<img src="https://www.dustloop.com/wiki/images/thumb/a/ac/GGST_Sin_Kiske_Icon.png/85px-GGST_Sin_Kiske_Icon.png" alt="Sin" />""",
    'Baiken': """<img src="https://www.dustloop.com/wiki/images/thumb/1/1c/GGST_Baiken_Icon.png/85px-GGST_Baiken_Icon.png" alt="Baiken" />""",
    'Anji': """<img src="https://www.dustloop.com/wiki/images/thumb/b/b2/GGST_Anji_Mito_Icon.png/85px-GGST_Anji_Mito_Icon.png" alt="Anji" />""",
    'Leo': """<img src="https://www.dustloop.com/wiki/images/thumb/6/64/GGST_Leo_Whitefang_Icon.png/85px-GGST_Leo_Whitefang_Icon.png" alt="Leo" />""",
    'Faust': """<img src="https://www.dustloop.com/wiki/images/thumb/f/f7/GGST_Faust_Icon.png/85px-GGST_Faust_Icon.png" alt="Faust" />""",
    'Axl': """<img src="https://www.dustloop.com/wiki/images/thumb/b/b6/GGST_Axl_Low_Icon.png/85px-GGST_Axl_Low_Icon.png" alt="Axl" />""",
    'Potemkin': """<img src="https://www.dustloop.com/wiki/images/thumb/f/f5/GGST_Potemkin_Icon.png/85px-GGST_Potemkin_Icon.png" alt="Potemkin" />""",
    'Giovanna': """<img src="https://www.dustloop.com/wiki/images/thumb/4/41/GGST_Giovanna_Icon.png/85px-GGST_Giovanna_Icon.png" alt="Giovanna" />""",
    'Goldlewis': """<img src="https://www.dustloop.com/wiki/images/thumb/e/e1/GGST_Goldlewis_Dickinson_Icon.png/85px-GGST_Goldlewis_Dickinson_Icon.png" alt="Goldlewis" />""",
    'Bridget': """<img src="https://www.dustloop.com/wiki/images/thumb/b/b5/GGST_Bridget_Icon.png/85px-GGST_Bridget_Icon.png" alt="Bridget" />"""
}

for x in char_img.keys():
    email_body = email_body.replace(x, char_img[x])

msg = MIMEMultipart()
msg['Subject'] = 'Matchups'
msg['From'] = "gaminggrandma@gmail.com"
msg['To'] = "purpleeyeballs21@gmail.com"


msg.attach(MIMEText(email_body, 'html'))
s = smtplib.SMTP_SSL('smtp.gmail.com')
s.login("purpleeyeballs21@gmail.com", open(r'C:\\Repos\\GG_Data\\pass.txt', 'r').read())
s.sendmail(msg['From'], msg['To'], str(msg))
s.quit()