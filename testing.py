import csv


def record_txt(data_list, filename, delimiter='\n'):
    my_file = open(filename, 'w')
    for elem in data_list:
        my_file.write(elem + delimiter)


def read_infile():
    with open('USA GF Value.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        j = 0
        for elem in data:
            data[j] = elem[0]
            j += 1
    return data

data = read_infile()

record_txt(data, 'USA GF Value.csv')
