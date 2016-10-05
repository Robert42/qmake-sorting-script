#!/bin/env python

from argparse import ArgumentParser


class Line:
    def __init__(self, content):
        self.content = content
        self.line_ending = '\n'
        if '\r\n' in self.content:
            self.line_ending = '\r\n'
            self.content = self.content.replace('\r\n', '')
        self.content = self.content.replace('\n', '')

    @property
    def whole_content(self) -> str:
        return self.content + self.line_ending


def resort_file(filename):
    lines = []
    with open(filename, 'rU') as file:
        for line in file:
            lines.append(Line(line))

    had_change = False

    if had_change:
        with open(filename, 'w') as file:
            for line in lines:
                file.write(line.whole_content)


def go():
    # https://docs.python.org/2/library/argparse.html
    parser = ArgumentParser(description='Resorts a qmake project file')
    parser.add_argument('--files', dest='files', metavar='FILES', type=str, nargs='+', help='A list of files to resort')
    args = parser.parse_args()

    for filename in args.files:
        resort_file(filename)


go()
