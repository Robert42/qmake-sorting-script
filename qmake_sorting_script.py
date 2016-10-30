#!/usr/bin/env python3

#This is free and unencumbered software released into the public domain.
#
#Anyone is free to copy, modify, publish, use, compile, sell, or
#distribute this software, either in source code form or as a compiled
#binary, for any purpose, commercial or non-commercial, and by any
#means.
#
#In jurisdictions that recognize copyright laws, the author or authors
#of this software dedicate any and all copyright interest in the
#software to the public domain. We make this dedication for the benefit
#of the public at large and to the detriment of our heirs and
#successors. We intend this dedication to be an overt act of
#relinquishment in perpetuity of all present and future rights to this
#software under copyright law.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
#OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#OTHER DEALINGS IN THE SOFTWARE.
#
#For more information, please refer to <http://unlicense.org>

from argparse import ArgumentParser
from copy import copy
from os import path
import re
import os

# https://docs.python.org/2/library/re.html
list_start_regex = re.compile(r'^\s*(?P<prefix>(:?[a-z_A-Z][a-z_A-Z0-9]*\:)*)(?P<name>[A-Z_]+)\s*(?P<assignment>\+?=)\s*(?P<values>.*\\?)\s*$')
value_analysis_regex = re.compile(r'^\s*(?P<rest>[^\\s\\][^\\]*)?\s*(?P<expect_next_line>\\)?\s*$')
value_seperation_regex = re.compile(r'^\s*(?P<file>[^\s]+)?\s*(?P<rest>.*)\s*$')


variables_to_resort = ['SOURCES', 'HEADERS', 'FORMS', 'RESOURCES']

verbose = False
print_resorted_files = False
move_inl_to_headers = False
move_inl_to_sources = False
dry_run = False
indentation = ''
projectfile_extensions = ['.pro', '.pri']

sorting_key = str.lower


class Line:
    def __init__(self, content):
        self.name = ''
        self.prefix = ''
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
        return len(self.name) > 0

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
            self.files.sort(key=sorting_key)
            if comparison != self.files:
                self._was_resorted = True
            return self._was_resorted
        else:
            return False

    def remove_inl_files(self):
        inl_files = []
        if self.is_resorted:
            other_files = []
            for file in self.files:
                basename, ext = path.splitext(file)
                if ext.lower() == '.inl':
                    inl_files.append(file)
                else:
                    other_files.append(file)
            self.files = other_files
        return inl_files

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
    if move_inl_to_headers or move_inl_to_sources:
        if move_inl_to_headers:
            target_name = 'HEADERS'
        elif move_inl_to_sources:
            target_name = 'SOURCES'

        all_inl_files = {}
        target_list = {}
        line_ending = '\n'
        for line in lines:
            line_ending = line.line_ending
            if line.name == target_name:
                target_list[line.prefix] = line
            else:
                if line.prefix not in all_inl_files:
                    all_inl_files[line.prefix] = []
                all_inl_files[line.prefix].extend(line.remove_inl_files())
        if len(all_inl_files) > 0:
            for key in sorted(all_inl_files.keys(), key=sorting_key):
                if len(all_inl_files[key]) > 0:
                    had_change = True
                    if key not in target_list:
                        target_list[key] = Line('{}{} = \\{}'.format(key, target_name, line_ending))
                        lines.append(target_list[key])
                    target_list[key].files.extend(all_inl_files[key])

    for line in lines:
        had_change = line.resort() or had_change

    if dry_run:
        if had_change:
            print('Would resort file {}'.format(filename))
        else:
            print('Would  skip  file {}'.format(filename))
        return

    if had_change:
        with open(filename, 'w') as file:
            for line in lines:
                file.write(line.whole_content)
        if print_resorted_files:
            print("resorted file {}".format(filename))


def excluded(file, excluded_dirs):
    for d in excluded_dirs:
        d = path.abspath(d)
        if file.startswith(d):
            return True
    return False


def go():
    global print_resorted_files
    global verbose
    global indentation
    global move_inl_to_headers
    global move_inl_to_sources
    global dry_run

    # https://docs.python.org/2/library/argparse.html
    parser = ArgumentParser(description='Resorts a qmake project file as a heuristic to reduce the risk of merge conflicts.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Add more verbose output for more easy debuggability')
    parser.add_argument('-p', '--print-resorted-files', dest='print_resorted_files', action='store_true', help='Print the filenames of the files, which were resorted')
    parser.add_argument('-i', '--indentation', default=4, help='How much spaces to add before each line break (default 4)')
    parser.add_argument('--move-inl-to-headers', action='store_true', help='If set, all inl files are moved to the HEADERS list (if existant)')
    parser.add_argument('--move-inl-to-sources', action='store_true', help='If set, all inl files are moved to the SOURCES list (if existant)')
    parser.add_argument('--files', dest='files', metavar='FILE', default=[], type=str, nargs='+', help='A list of files to resort')
    parser.add_argument('-r', '--include-recursive', metavar='PATH', default=[], type=str, nargs='+', help='A list of directories to search for *.pro and *.pri files to resort')
    parser.add_argument('-e', '--exclude-recursive', metavar='PATH', default=[], type=str, nargs='+', help='A list of directories to exclude from the search for *.pro and *.pri files to resort')
    parser.add_argument('-n', '--dry-run', action='store_true', help="Don't change anything, just print the project files, which would be resorted")
    args = parser.parse_args()

    verbose = args.verbose
    dry_run = args.dry_run
    print_resorted_files = args.print_resorted_files or verbose
    move_inl_to_headers = args.move_inl_to_headers
    move_inl_to_sources = args.move_inl_to_sources
    indentation = ''

    if move_inl_to_headers and move_inl_to_sources:
        print("WARNING: --move-inl-to-headers and --move-inl-to-sources used at the same time!")

    for i in range(0, args.indentation):
        indentation += ' '

    files_to_sort = args.files

    for included_dir in args.include_recursive:
        included_dir = path.abspath(included_dir)
        for root, dirs, files in os.walk(included_dir):
            for file in files:
                file = path.join(root, file)
                basename, ext = path.splitext(file)
                if ext.lower() in projectfile_extensions and not excluded(file, args.exclude_recursive):
                    files_to_sort.append(file)

    if len(files_to_sort) == 0:
        print("Nothing to sort")

    for filename in files_to_sort:
        resort_file(filename)


go()
