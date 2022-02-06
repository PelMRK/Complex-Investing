import pyautogui as pag
import pyperclip
import time
import csv


def buffer():
    res = pyperclip.paste()
    return res


def record_outfile(data_list):
    my_file = open('Extended Insights.csv', 'w')
    for elem in data_list:
        my_file.write(elem[0] + ';' + elem[1] + '\n')


def read_infile():
    with open('Extended Insights.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        j = 0
        for elem in data:
            data[j] = elem[0]
            j += 1
    return data


times = []

links = read_infile()
for i in range(len(links)):
    links[i] = links[i].split(';')
starting = 0
for kk in range(len(links)):
    if links[kk][1] == '':
        starting = kk
        break
pag.sleep(1)
for i in range(starting, len(links)):
    pyperclip.copy('')
    start_time = time.time()
    pag.sleep(0.6)
    url_ = links[i][0]
    url_ = "view-source:" + url_.replace("ru.", "")
    url_ = url_.replace("analysts&source=desktop&medium=instrument", "") + "smart-score"
    url_ = url_.replace("analysts", "")
    pag.hotkey('ctrl', 'l')
    pag.sleep(0.3)
    pag.write(url_)
    pag.sleep(0.35)
    pag.press('enter')
    pag.sleep(0.35)
    while pag.screenshot().getpixel((37, 12)) != (75, 75, 75):
        pag.sleep(0.5)
    pag.sleep(0.6)
    pag.hotkey('ctrl', 'a')
    pag.sleep(0.5)
    pag.hotkey('ctrl', 'c')
    pag.sleep(0.5)
    whole_code = buffer()
    flag = False
    score_rate = 'error'
    if '<tspan x="100" text-anchor="middle" stroke-width="0" fill="black">' in whole_code:
        flag = True
    if flag:
        score_rate = whole_code.split('<tspan x="100" text-anchor="middle" stroke-width="0" fill="black">')
        score_rate = (score_rate[1])[0:2].replace('<', "")
        links[i][1] = score_rate
    else:
        links[i][1] = '0'

    record_outfile(links)
    pag.sleep(1)
    times.append(time.time() - start_time)
    average_sec = sum(times) / len(times)
    print(round(i/len(links)*100, 2), "% ;\tleft:", round(average_sec * (len(links) - i) / 3600, 2), "hours")
