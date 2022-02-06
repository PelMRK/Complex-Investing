import pyautogui as pag
import time
import csv
import pyperclip


def buffer():
    res = pyperclip.paste()
    return res


def record_outfile(data_list):
    my_file = open('Insights.csv', 'w')
    for elem in data_list:
        my_file.write(elem[0] + ';' + elem[1] + '\n')


def read_infile():
    with open('Insights.csv', newline='') as f:
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
    start_time = time.time()
    pyperclip.copy('')
    pag.sleep(0.3)
    pag.hotkey('ctrl', 'l')
    pag.sleep(0.1)
    pag.write("view-source:" + links[i][0])
    pag.sleep(0.2)
    pag.press('enter')
    pag.sleep(0.5)
    while pag.screenshot().getpixel((37, 12)) != (75, 75, 75):
        pag.sleep(0.5)
    pag.sleep(0.75)
    pag.hotkey('ctrl', 'a')
    pag.sleep(0.5)
    pag.hotkey('ctrl', 'c')
    pag.sleep(0.75)
    whole_code = buffer()
    try:
        price = whole_code.split('"priceTarget":')
        price = (price[1].split(','))[0]
    except IndexError:
        price = 'err'
    print(price, "- price")

    links[i][1] = price

    record_outfile(links)
    times.append(time.time() - start_time)
    average_sec = sum(times) / len(times)
    if i == len(links)//2:
        pag.sleep(200)
    elif i % 200 == 0:
        pag.sleep(40)
    elif i % 50 == 0:
        pag.sleep(10)
    else:
        pag.sleep(2.6)  # Не надо ускорять, а то заблокируют
    print(round(i / len(links) * 100, 2), "% ;\tleft:", round(average_sec * (len(links) - i) / 3600, 2), "hours")
