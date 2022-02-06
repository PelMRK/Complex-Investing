import pyautogui as pag
import time
import pyperclip
import csv


def record_outfile(data_list):
    my_file = open('USA GF Value.csv', 'w')
    for elem in data_list:
        my_file.write(elem[0] + ';' + elem[1] + '\n')


def read_infile():
    with open('USA GF Value.csv', newline='') as f:
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
    pag.sleep(0.3)
    pag.hotkey('ctrl', 'l')
    pag.sleep(0.25)
    pag.write(links[i][0])
    pag.sleep(0.3)
    pag.press('enter')
    while pag.screenshot().getpixel((35, 17)) != (255, 255, 255):
        pag.sleep(0.05)
    while pag.screenshot().getpixel((1585, 645))[0] == 102:
        pag.sleep(0.05)


    def code():
        while pag.screenshot().getpixel((37, 12)) != (23, 66, 123) and pag.screenshot().getpixel((1585, 645))[0] != 102:
            pag.sleep(0.5)

        pag.moveTo(1585, 645, 0.5)

        k = 0
        while pag.screenshot().getpixel((1585, 645))[0] != 102:
            pag.sleep(3)
            k += 1
            if k == 5:
                pag.moveTo(500, 380, 1)
                pag.sleep(0.2)
                pag.tripleClick()
                pag.sleep(0.1)
                pag.hotkey('ctrl', 'c')

                if 'GF Value : $0.00 (As of Today)' in pyperclip.paste():
                    print("NO DATA - 0")
                    links[i][1] = '0'
                    return

        pag.sleep(0.26)
        pag.click()
        pag.moveTo(1500, 900, 0.5)
        pag.click()
        pag.sleep(0.5)
        while pag.screenshot().getpixel((220, 220)) != (177, 213, 221):
            pag.sleep(0.5)
        pag.hotkey('ctrl', 'end')
        pag.sleep(0.1)
        pag.moveTo(380, 860, 0.1)
        pag.doubleClick()
        pag.sleep(0.1)
        pag.hotkey('ctrl', 'c')
        pag.sleep(0.25)
        pag.hotkey('alt', 'f4')
        price = pyperclip.paste().split(";")
        try:
            links[i][1] = price[2].replace(',', '.')
        except IndexError:
            links[i][1] = '0'
        pag.sleep(2)


    code()
    record_outfile(links)

    times.append(time.time() - start_time)
    average_sec = sum(times) / len(times)
    print(round(i / len(links) * 100, 2), "% ;\tleft:", round(average_sec * (len(links) - i) / 3600, 2), "hours")

