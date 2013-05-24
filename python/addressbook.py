#!/usr/bin/python

import argparse
import csv
import os
import requests

def readData(dataPath, outputPath):
    ifile  = open(dataPath, 'r')
    reader = csv.reader(ifile, delimiter=';')
	
    rownum = 0
    for row in reader:
        # Save header row.
        if rownum == 0:
            header = row
        else:
            colnum = 0
            dict = {}
            for col in row:
                dict[header[colnum]] = col;
                colnum += 1
            meCard = 'MECARD:N:%s;ADR:%s;TEL:+%s;EMAIL:%s;;' % (dict['name'], dict['address'], dict['phone'], dict['email'])
            fetchQRCode(meCard, outputPath, dict['name'] + '.png')
			
        rownum += 1
    ifile.close()
	
def fetchQRCode(meCard, outputPath, fileName):
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    r = requests.get('https://chart.googleapis.com/chart?chs=150x150&cht=qr&chl=%s' % (meCard))
    if r.status_code == 200:
        with open(outputPath + '\\' + fileName, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

def main():
    parser = argparse.ArgumentParser(description='Create a formatted address book.')
    parser.add_argument('dataPath', metavar='dataPath', nargs=1, help='Path to the data file to import')
    parser.add_argument('outputPath', metavar='outputPath', nargs=1, default='output', help='The path of the output')
    parser.add_argument('--type', choices=['csv'], default='csv', help='Type of the data used')
    parser.add_argument('--size', type=int, default='150', help='The size of the QR code to generate')
    
    args = parser.parse_args()
    readData(args.dataPath[0], args.outputPath[0])

if __name__ == "__main__":
    main()
