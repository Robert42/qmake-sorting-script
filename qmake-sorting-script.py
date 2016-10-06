#!/usr/bin/env python3

from argparse import ArgumentParser
from copy import copy
import re

# https://docs.python.org/2/library/re.html
list_start_regex = re.compile(r'^\s*(?P<prefix>(:?[a-z_A-Z][a-z_A-Z0-9]*\:)*)(?P<name>[A-Z_]+)\s*(?P<assignment>\+?=)\s*(?P<values>.*\\?)\s*$')
value_analysis_regex = re.compile(r'^\s*(?P<rest>[^\\s\\][^\\]*)?\s*(?P<expect_next_line>\\)?\s*$')
value_seperation_regex = re.compile(r'^\s*(?P<file>[^\s]+)?\s*(?P<rest>.*)\s*$')


variables_to_resort = ['SOURCES', 'HEADERS', 'FORMS', 'RESOURCES']

verbose = False
print_resorted_files = False
move_inl_to_headers = False
move_inl_to_sources = False
indentation = ''


class Line:
    def __init__(self, content):
        if '\r\n' in content:
            self.line_ending = '\r\n'
        else:
            self.line_ending = '\n'
        content = content.replace(self.line_ending, '')

        match = list_start_regex.match(content)

        if match:
            if verbose:
                print('Line {}'.format(content))
            prefix = match.group('prefix')
            name = match.group('name')
            assignment = match.group('assignment')
            values = match.group('values')

            if name in variables_to_resort:
                self.prefix = prefix
                self.name = name
                self.assignment = assignment
                self.files = []
                self.expect_next_line = True
                self._was_resorted = False
                self.append_line(values)
                if verbose:
                    print('self.name {}'.format(self.name))
                    print('self.assignment {}'.format(self.assignment))
                return
        self.expect_next_line = False
        self.content = content

    @property
    def whole_content(self) -> str:
        if self.is_resorted:
            return self._format_list()
        else:
            return self.content + self.line_ending

    @property
    def is_resorted(self) -> bool:
        return hasattr(self, 'name')

    def append_line(self, line):
        line = line.replace(self.line_ending, '')
        rest = line
        match = value_analysis_regex.match(rest)
        if match:
            self.expect_next_line = not match.group('expect_next_line') is None
            if verbose:
                print('line {}'.format(line))
                print('self.expect_next_line {}'.format(self.expect_next_line))
            rest = match.group('rest')
            while rest:
                match = value_seperation_regex.match(rest)
                self.files.append(match.group('file'))
                rest = match.group('rest')
        else:
            self.expect_next_line = False

    def resort(self):
        if self.is_resorted:
            comparison = copy(self.files)
            self.files.sort()
            if comparison != self.files:
                self._was_resorted = True
            return self._was_resorted
        else:
            return False

    def _format_list(self):
        result = ['{} {}'.format(self.prefix + self.name, self.assignment)]
        result.extend(self.files)
        if verbose:
            print('self.files {}'.format(self.files))
            print(result)
        result = (' \\\n'+indentation).join(result) + '\n'
        if verbose:
            print(result)
        return result


def resort_file(filename):
    last_line = Line('')

    lines = []
    with open(filename, 'rU') as file:
        for line in file:
            if last_line.expect_next_line:
                last_line.append_line(line)
            else:
                last_line = Line(line)
                lines.append(last_line)

    had_change = False
    for line in lines:
        had_change = had_change or line.resort()

    if had_change:
        with open(filename, 'w') as file:
            for line in lines:
                file.write(line.whole_content)
        if print_resorted_files:
            print("resorted file {}".format(filename))


def go():
    global print_resorted_files
    global verbose
    global indentation
    global move_inl_to_headers
    global move_inl_to_sources

    # https://docs.python.org/2/library/argparse.html
    parser = ArgumentParser(description='Resorts a qmake project file as a heuristic to reduce the risk of merge conflicts.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Add more verbose output for more easy debuggability')
    parser.add_argument('-p', '--print-resorted-files', dest='print_resorted_files', action='store_true', help='Print the filenames of the files, which were resorted')
    parser.add_argument('-i', '--indentation', default=4, help='How much spaces to add before each line break')
    parser.add_argument('--move-inl-to-headers', action='store_true', help='If set, all inl files are moved to the HEADERS list (if existant)')
    parser.add_argument('--move-inl-to-sources', action='store_true', help='If set, all inl files are moved to the SOURCES list (if existant)')
    parser.add_argument('--files', dest='files', metavar='FILES', default=[], type=str, nargs='+', help='A list of files to resort')
    args = parser.parse_args()

    verbose = args.verbose
    print_resorted_files = args.print_resorted_files or verbose
    move_inl_to_headers = args.move_inl_to_headers
    move_inl_to_sources = args.move_inl_to_sources
    indentation = ''
    for i in range(0, args.indentation):
        indentation += ' '

    for filename in args.files:
        resort_file(filename)


go()
