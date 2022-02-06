import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
import csv


def read_infile():
    with open('infile.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        j = 0
        for elem in data:
            data[j] = elem[0]
            j += 1
    return data


end = 1667  # "Число с сайта" минус один
symbols = read_infile()
tickers = pd.Series()
update = pd.Series()
req = requests.get("https://www.tinkoff.ru/invest/stocks/?country=Foreign&orderType=Asc&sortType=ByName&start=0&end="
                   + str(end))
if req.status_code != 200:
    quit()
soup = BeautifulSoup(req.content, 'html.parser')
dom = etree.HTML(str(soup))
ticks = soup.find_all('div', class_='Caption__subcaption_seofa')  # Поменять класс, если не находит
print(len(ticks))
for row in range(len(ticks)):
    # test = dom.xpath('/html/body/div[1]/div/div[3]/div/div[1]/div/div[4]/div[1]/div/a[' + str(row)
    #                  + ']/span/div/div/div[1]/div/div/div/div[2]/div/div[2]')
    test = ticks[row].text
    print(test)
    tickers.loc[len(tickers)] = test
    if test not in symbols:
        update.loc[len(update)] = test
    print(round(row/end*100, 2), '%')

# tickers.to_csv("tickers.csv")
update.to_csv("tickers.csv")
