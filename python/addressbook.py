#!/usr/bin/python

import argparse
import csv
import os
import requests
import unicodedata
import urllib

# Define constants
# Theses constants represents the header of the column in the dataset.
# The header of your csv file must match theses constant in order for program to output the appropriate latex content.

FIRST_NAME = 'firstname'
LAST_NAME = 'lastname'
NICK_NAME = 'nickname'
PROGRAM_OF_STUDIES = 'studies'
BIRTHDAY = 'birthday'
ADDRESS = 'address'
PHONE = 'phone'
EMAIL = 'email'
FAVORITE_QUOTE = 'quote'

def strip_accents(s):
    """Sanitize the provided string to remove accents."""
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def readData(dataPath, outputPath, qrCodeSize):
    """Method to read the CSV file and output the latex file.
    Parameters:
    dataPath   -- The path to the CSV file containing the information to include in the address book.
    outputPath -- The path to the folder to output the latex file and all the QR code. The latex file will be named 'address.tex'
    qrCodeSize -- The size of the QR code to produce.
    """

    # Open the csv "raw" data and read it.
    ifile  = open(dataPath, 'r', encoding="utf8")
    reader = csv.reader(ifile, delimiter=';')
    
    # Open the tex file to output the adresses.
    latex_writer = open(outputPath + 'address.tex', 'w', encoding="utf8")
    
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

            # Set all the information extracted from the current CSV record.
            firstname = dict[FIRST_NAME].strip()        # mandatory
            lastname = dict[LAST_NAME].strip()          # mandatory
            nickname = dict.get(NICK_NAME, '')          # optional
            studies = dict.get(PROGRAM_OF_STUDIES, '')  # optional
            birthday = dict.get(BIRTHDAY, '')             # optional
            address = dict.get(ADDRESS, '')             # optional
            phone = dict.get(PHONE, '')                 # optional
            email = dict.get(EMAIL, '')                 # optional
            quote = dict.get(FAVORITE_QUOTE, '')        # optional

            # Set composed information
            fullname = firstname + ' ' + lastname

            ## Create the meCard format for the QR code.

            # The value must be sanitize for the meCard format
            meCardFullname = fullname.replace(",", "")
            meCardAddress = address.replace(",", "") 
            meCardPhone = address.replace(",", "")
            meCardEmail = address.replace(",", "")

            meCard = 'MECARD:N:%s;ADR:,,%s,,,,;TEL:%s;EMAIL:%s;;' % (meCardFullname, meCardAddress, meCardPhone, meCardEmail)
            meCard = urllib.parse.quote(strip_accents(meCard))
            qrcode_filename = strip_accents(fullname) + '.png'
            fetchQRCode(meCard, outputPath, qrcode_filename, qrCodeSize)
            
            # Create the latex entry with the macro.
            latex_entry = '\makeaddress[firstname={%s},lastname={%s},nickname={%s},studies={%s},birthday={%s},address={%s},phone={%s},email={%s},quote={%s},qrcode={photo/%s}]' % (firstname, lastname, nickname, studies,birthday, address, phone, email, quote, qrcode_filename)

            # Sanitize the produced latex (some people like to put "\epsilon" in their quote...)
            latex_entry = latex_entry.replace("_", "\_")
            latex_entry = latex_entry.replace("#", "\#")

            latex_writer.write(latex_entry + '\n\n\\bigskip\n\n')
        rownum += 1
    ifile.close()
    
def fetchQRCode(meCard, outputPath, fileName, qrCodeSize):
    """Get a QR code using the Google API (hopefully this will not get deprecated in the future :/ )

    Keyword arguments:
    meCard     -- the content of the QR code, see http://theqrplace.wordpress.com/2011/05/02/qr-code-tech-info-mecard-format/ for information on the meCard format.
    outputPath -- The path to output the image produced by the google API.
    fileName   -- The name of the file to output.
    qrCodeSize -- The size, in pixels, of the QR code to produce.
    """
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    # "%EF%BB%BF" is the BOM header, it must be sent at the start of the string to allow non-ASCII character.
    r = requests.get('https://chart.googleapis.com/chart?chs=%dx%d&cht=qr&choe=ISO-8859-1&chl=%s' % (qrCodeSize, qrCodeSize, meCard))
    if r.status_code == 200:
        with open(outputPath + '\\' + fileName, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

def main():
    """Main method of the program, defines the argument needed for the script to run."""
    parser = argparse.ArgumentParser(description='Create a formatted address book.')
    parser.add_argument('dataPath', metavar='dataPath', nargs=1, help='Path to the data file to import')
    parser.add_argument('outputPath', metavar='outputPath', nargs=1, default='output', help='The path of the output')
    parser.add_argument('--type', choices=['csv'], default='csv', help='Type of the data used')
    parser.add_argument('--size', type=int, default='500', help='The size of the QR code to generate')
    
    args = parser.parse_args()
    readData(args.dataPath[0], args.outputPath[0], args.size)

if __name__ == "__main__":
    main()
