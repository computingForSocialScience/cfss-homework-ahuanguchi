import csv
import sys

import pylab

def readCSV(filename):
    '''Reads the CSV file `filename` and returns a list
    with as many items as the CSV has rows. Each list item 
    is a tuple containing the columns in that row as stings.
    Note that if the CSV has a header, it will be the first
    item in the list.'''
    with open(filename,'r') as f:
        rdr = csv.reader(f)
        lines = list(rdr)
    return(lines)


### enter your code below

def get_avg_latlng(csv_lines):
    all_lat, all_long = [], []
    for line in csv_lines:
        if line[128] != '' and line[128][-1].isdigit():
            all_lat.append(float(line[128]))
        if line[129] != '' and line[129][-1].isdigit():
            all_long.append(float(line[129]))
    avg_lat = sum(all_lat) / len(all_lat)
    avg_long = sum(all_long) / len(all_long)
    print('Average latitude and longitude: (%s, %s)' % (avg_lat, avg_long))

def zip_code_barchart(csv_lines, save_file='barchart.jpg',
                      additional_info=' in permits_hydepark.csv'):
    zipcode_columns = [28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126]
    zipcodes = []
    for line in csv_lines:
        for column in zipcode_columns:
            zipcode = line[column]
            if zipcode != '' and zipcode[0].isdigit():
                zipcodes.append(zipcode[:5])    # remove everything after first 5 characters
    zip_set = sorted(set(zipcodes))    # sorted list of unique zip codes
    zip_counts = [zipcodes.count(zipcode) for zipcode in zip_set]
    index = range(1, len(zip_set) + 1)
    fig = pylab.figure()
    fig.set_size_inches(18, 9)
    ax = fig.add_subplot(111)
    ax.tick_params(axis='x', labelsize=10)
    ax.bar(index, zip_counts)
    ax.set_title('Counts of Contractor Zip Codes' + additional_info)
    ax.set_xticks(index)
    ax.set_xticklabels(zip_set, rotation=60)
    fig.savefig(save_file)

def command_line():
    """Use 'latlong' or 'hist' after 'parse.py' to call a function."""
    try:
        command = sys.argv[1]
        csv_file = sys.argv[2] if (len(sys.argv) >= 3) else 'permits_hydepark.csv'
        permits = readCSV(csv_file)
    except IndexError:
        command = None
    if command == 'latlong':
        get_avg_latlng(permits)
    elif command == 'hist':
        file = sys.argv[3] if (len(sys.argv) >= 4) else 'barchart.jpg'
        info = sys.argv[4] if (len(sys.argv) >= 5) else ' in permits_hydepark.csv'
        zip_code_barchart(permits, file, info)
        print('Bar chart created!')
    else:
        print("Use 'latlong' or 'hist' after 'parse.py' to call a function.")

def _find_zipcode_headers():
    '''Find the indices of zipcode headers and print them to a file as a list.'''
    original = readCSV('permits.csv')
    headers = original[0]
    zipcode_columns = []
    zipcode_column_names = []
    for i in xrange(len(headers)):
        if 'ZIPCODE' in headers[i]:
            zipcode_columns.append(i)
            zipcode_column_names.append(headers[i])
    with open('header_indices.txt', 'w') as file:
        file.write(str(zipcode_columns) + '\n\n')
        file.write(str(zipcode_column_names))

def _test():
    permits = readCSV('permits_hydepark.csv')
    get_avg_latlng(permits)
    zip_code_barchart(permits)

if __name__ == '__main__':
    # _find_zipcode_headers()
    # _test()
    command_line()
