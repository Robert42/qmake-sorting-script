#!/bin/env python

def resort_file(filename):
    with open(filename, 'rU') as file:
        for line in file:
            print(line.replace('\n', ''))


from argparse import ArgumentParser

#https://docs.python.org/2/library/argparse.html
parser = ArgumentParser(description='Resorts a qmake project file')
parser.add_argument('--files', dest='files', metavar='FILES', type=str, nargs='+', help='A list of files to resort')
args = parser.parse_args()

for filename in args.files:
    resort_file(filename)