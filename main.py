import requests
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd
import time
from lxml import etree
# Задачи:
# More Statistics
# Analyst Estimate
# Forward PE is null somehow + forward dividend


def record_txt(data_list, filename, delimiter='\n'):
    my_file = open(filename, 'w')
    for elem in data_list:
        my_file.write(elem + delimiter)


def read_txt(filename, delimiter='\n'):
    with open(filename, 'r') as f:
        lines = f.read().split(delimiter)
        lines = lines[:-1]
    return lines


def record_outfile(data):
    data.to_csv('outfile.csv')


def read_infile():
    with open('infile.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        j = 0
        for elem in data:
            data[j] = elem[0]
            j += 1
    return data


def special_check(xpath, val_):
    result = "error"
    l_xpath = xpath.split("td")
    l_xpath = l_xpath[0] + "td[1]/a"
    l_xpath = l_xpath.split("/tr")
    try:
        for num in range(1, 100):
            new_xp = l_xpath[0] + "/tr[" + str(num) + "]/td[1]/a"
            if dom.xpath(new_xp)[0].text.replace("\n", "") == val_:
                xpath = xpath.split("/tr")
                xpath[1] = xpath[1][xpath[1].find("]"):]
                new_xp = xpath[0] + "/tr[" + str(num) + xpath[1]
                result = dom.xpath(new_xp)[0].text
                result = result.replace(" ", "").replace(".", ",").replace("%", "")
                result = result.replace("ROIC", "").replace("WACC", "").replace("\n", "")
    except IndexError:
        return result
    return result


def special_check2(xpath, val_):
    result = "error"
    per = ""
    if '_ind' in val_:
        per = 1
    elif '_his' in val_:
        per = 2
    try:
        for num in range(per, 100, 2):
            xml = xpath + str((num+1)//2) + ']/td[' + str(4-count % 2) + ']/div/div'
            xml2 = xml.replace("td[3]", "td[1]").replace("td[4]", "td[1]").replace("/div/div", "/a")
            label = dom.xpath(xml2)[0].text.replace("\n", "")
            if label == val_.replace("_ind", "").replace("_his", ""):
                result = dom.xpath(xml)[0].get("style")
                result = result[result.find(":") + 1:result.find("%")].replace(".", ",")
    except IndexError:
        return result
    return result


times = []
symbols = read_infile()
# symbols = ["H", "HDGgzA", "HAE"]

ls = read_txt('data/ls.txt')
ls_a = read_txt('data/ls_a.txt')
ls_div = ["Volume:", "Avg Vol (1m):", "Market Cap $:", "Enterprise Value $:"]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/93.0.4577.82 Safari/537.36'}
df = pd.DataFrame(columns=ls)
i = 0

for t in symbols:
    i += 1
    start_time = time.time()
    scores = [t]
    req = requests.get("https://www.gurufocus.com/stock/" + t)
    if req.status_code != 200:
        df.loc[len(df)] = ""
        print(t, "Failed")
        continue
    soup = BeautifulSoup(req.content, 'html.parser')
    count = 1
    for val in ls[1:]:
        try:
            dom = etree.HTML(str(soup))
            if val in ls_a:
                one = soup.find('a', string=re.compile(val)).find_next('td').text.replace("\n", "").replace("/10", "")
                one = one.replace(".", ",").replace(" ", "")
                scores.append(one)
            elif val in ls_div:
                head_ = soup.find('div', class_='stock-summary-table fc-regular').text
                head_ = head_.replace("\n", "")
                head_ = head_[:head_.find(" PE")]
                head = (head_.split(val))[1]
                head = head[3:]
                head = head[:head.find("   ")].replace(",", "")
                if 'Til' in head:
                    head = str(float(head[:-4]) * 1000)[:-2]
                elif 'Bil' in head:
                    head = head[:-4].replace(".", ",")
                elif 'Mil' in head:
                    head = str(float(head[:-4]) / 1000).replace(".", ",")
                scores.append(head)
            elif val == 'Buffet Stars':
                stars = str(soup.find('div', class_='stock-rate'))
                stars = stars[stars.find("aria-valuenow") + 15:]
                stars = stars[:stars.find('"')].replace(".", ",")
                scores.append(stars)
            elif val == 'ROC (Joel Greenblatt) %':
                roc = special_check('//*[@id="profitability"]/div/table[2]/tbody/tr[5]/td[2]', val)
                scores.append(roc)
            elif val == 'Price-to-Intrinsic-Value-DCF (Earnings Based)':
                pivd = special_check('//*[@id="valuation"]/div/table[2]/tbody/tr[3]/td[2]', val)
                scores.append(pivd)
            elif val == 'Earnings Yield (Greenblatt) %':
                ey_g = special_check('//*[@id="valuation"]/div/table[2]/tbody/tr[7]/td[2]', val)
                scores.append(ey_g)
            elif val == 'Forward Rate of Return (Yacktman) %':
                frr_y = special_check('//*[@id="valuation"]/div/table[2]/tbody/tr[8]/td[2]', val)
                scores.append(frr_y)
            elif val == 'ROIC':
                roic = special_check('//*[@id="financial-strength"]/div/table[2]/tbody/tr[9]/td[3]/div/div/div[1]/div',
                                     "WACC vs ROIC")
                scores.append(roic)
            elif val == 'WACC':
                wacc = special_check('//*[@id="financial-strength"]/div/table[2]/tbody/tr[9]/td[3]/div/div/div[2]/div',
                                     "WACC vs ROIC")
                scores.append(wacc)
            elif val == 'roic - wacc':
                sub = float(scores[-2].replace(",", ".")) - float(scores[-1].replace(",", "."))
                sub = str(sub).replace(".", ",")
                scores.append(sub)
            # elif val == 'Revenue (TTM) (Mil $)':
            #     # m_s = soup.find('#text', string=re.compile(val)).find_next('span')
            #     # m_s = dom.xpath('/html/body/div[1]/div/div/div[1]/section[2]/main/div/section/main/div[2]/div[2]/div')[0].text
            #     m_s = soup.find_all('div', class_="statictics-item")
            #     print(m_s)
            #     scores.append(m_s)
            elif "_ind" in val or "_his" in val:
                ind_his = ""
                if count < 11:
                    ind_his = special_check2('//*[@id="financial-strength"]/div/table[2]/tbody/tr[', val)
                elif 11 <= count < 27:
                    ind_his = special_check2('//*[@id="profitability"]/div/table[2]/tbody/tr[', val)
                elif 27 <= count < 63:
                    ind_his = special_check2('//*[@id="ratios"]/div/table[2]/tbody/tr[', val)
                elif 63 <= count < 75:
                    ind_his = special_check2('//*[@id="dividend"]/div/table[2]/tbody/tr[', val)
                elif 75 <= count < 91:
                    ind_his = special_check2('//*[@id="valuation"]/div/table[2]/tbody/tr[', val)
                count += 1
                scores.append(ind_his)
            else:
                print("Raised Exception")
                quit()
        except (AttributeError, IndexError, ValueError):
            scores.append('error')
    df.loc[len(df)] = scores
    if i % 50 == 0:
        record_outfile(df)
    times.append(time.time() - start_time)
    average_sec = sum(times) / len(times)
    print(t, ";\t", round(i / len(symbols) * 100, 2), "% ;\tleft:", round(average_sec * (len(symbols) - i) / 3600, 2),
          "hours")

record_outfile(df)
