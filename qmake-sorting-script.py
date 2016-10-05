#!/bin/env python

from argparse import ArgumentParser


def resort_file(filename):
    lines = []
    line_ending = '\n'
    with open(filename, 'rU') as file:
        for line in file:
            if '\r\n' in line:
                line_ending = '\r\n'
                line = line.replace('\r\n', '')
            line = line.replace('\n', '')
            lines.append(line)

    had_change = False

    if had_change:
        with open(filename, 'w') as file:
            for line in lines:
                line += line_ending
                file.write(line)


def go():
    # https://docs.python.org/2/library/argparse.html
    parser = ArgumentParser(description='Resorts a qmake project file')
    parser.add_argument('--files', dest='files', metavar='FILES', type=str, nargs='+', help='A list of files to resort')
    args = parser.parse_args()

    for filename in args.files:
        resort_file(filename)


go()
