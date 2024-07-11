import pandas as pd
import requests
from bs4 import BeautifulSoup as bfs
from io import StringIO
from pathlib import Path

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }
DATA_PATH = 'data/fiis.csv'

class CollectDataFromSite():
    def __init__(self) -> None:
        self.url = "https://fundamentus.com.br/fii_resultado.php"
        self.df = pd.DataFrame()
        self.__buildDataFrame()

    def __get_data(self):
        response = requests.get(url=self.url,headers=HEADERS)
        return response.text

    def __format_table(self):
        soup = bfs(self.__get_data(),'html.parser')
        table = soup.find('table')
        str_table = str(table)
        str_table = str_table.replace("%",'')
        str_table = str_table.replace(".",'')
        return str_table

    def __buildDataFrame(self):
        self.df = pd.read_html(StringIO(self.__format_table()),decimal=',')[0]
        self.__normalizeColumns()
        return self.df
    
    def __normalizeColumns(self):
        columns = self.get_columns()
        columns.remove('Papel')
        columns.remove('Segmento')
        columns.remove('Qtd de imóveis')
        columns.remove('Liquidez')
        columns.remove('Valor de Mercado')

        for column in columns:
            self.df[column] = self.df[column]/100
    
    def get_columns(self):
        return list(self.df.columns)
    
    def get_papeis(self):
        return list(self.df['Papel'])

    def visualize_data(self):
        print(self.df['Valor de Mercado'].max())
        print("*"*10)
        print(self.df.info())

    def saveData(self):
        self.df.to_csv(DATA_PATH)

data = CollectDataFromSite()
data.visualize_data()
data.saveData()