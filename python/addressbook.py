#!/usr/bin/python

import argparse
import csv
import os
import requests

def readData(dataPath, outputPath, qrCodeSize):
    ifile  = open(dataPath, 'r')
    reader = csv.reader(ifile, delimiter=';')
	
    latex_writer = open(outputPath + 'address.tex', 'w')
	
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
            name = dict['firstname'] + ' ' + dict['lastname']
            meCard = 'MECARD:N:%s;ADR:%s;TEL:+%s;EMAIL:%s;;' % (name, dict.get('address',''), dict.get('phone',''), dict.get('email',''))
            qrcode_filename = name + '.png'
            fetchQRCode(meCard, outputPath, qrcode_filename, qrCodeSize)
			
            latex_entry = '\makeaddress[firstname={%s},lastname={%s},nickname={%s},studies={%s},birthday={%s},address={%s},phone={%s},email={%s},quote={%s},qrcode={%s}]' % (dict['firstname'],  dict['lastname'], dict.get('nickname',''), dict.get('studies',''),dict.get('birthday',''), dict.get('address',''), dict.get('phone',''), dict.get('email',''), dict.get('quote',''), qrcode_filename)
            latex_writer.write(latex_entry + '\n\n\\bigskip\n\n')
			
        rownum += 1
    ifile.close()
	
def fetchQRCode(meCard, outputPath, fileName, qrCodeSize):
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    r = requests.get('https://chart.googleapis.com/chart?chs=%dx%d&cht=qr&chl=%s' % (qrCodeSize, qrCodeSize, meCard))
    if r.status_code == 200:
        with open(outputPath + '\\' + fileName, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

def main():
    parser = argparse.ArgumentParser(description='Create a formatted address book.')
    parser.add_argument('dataPath', metavar='dataPath', nargs=1, help='Path to the data file to import')
    parser.add_argument('outputPath', metavar='outputPath', nargs=1, default='output', help='The path of the output')
    parser.add_argument('--type', choices=['csv'], default='csv', help='Type of the data used')
    parser.add_argument('--size', type=int, default='100', help='The size of the QR code to generate')
    
    args = parser.parse_args()
    readData(args.dataPath[0], args.outputPath[0], args.size)

if __name__ == "__main__":
    main()
