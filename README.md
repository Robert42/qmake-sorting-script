# qmake-sorting-script
Script for sorting qmake files.

## Usage

If you want to resort all qmake project files found recursively in */path/to/my/project*, just run the script with:

    qmake-sorting-script.py -r /path/to/my/project


Overview over all possible arguments


```
usage: qmake-sorting-script.py [-h] [-v] [-p] [-i INDENTATION]
                               [--move-inl-to-headers] [--move-inl-to-sources]
                               [--files FILE [FILE ...]] [-r PATH [PATH ...]]
                               [-e PATH [PATH ...]] [-n]

Resorts a qmake project file as a heuristic to reduce the risk of merge
conflicts.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Add more verbose output for more easy debuggability
  -p, --print-resorted-files
                        Print the filenames of the files, which were resorted
  -i INDENTATION, --indentation INDENTATION
                        How much spaces to add before each line break (default
                        4)
  --move-inl-to-headers
                        If set, all inl files are moved to the HEADERS list
                        (if existant)
  --move-inl-to-sources
                        If set, all inl files are moved to the SOURCES list
                        (if existant)
  --files FILE [FILE ...]
                        A list of files to resort
  -r PATH [PATH ...], --include-recursive PATH [PATH ...]
                        A list of directories to search for *.pro and *.pri
                        files to resort
  -e PATH [PATH ...], --exclude-recursive PATH [PATH ...]
                        A list of directories to exclude from the search for
                        *.pro and *.pri files to resort
  -n, --dry-run         Don't change anything, just print the project files,
                        which would be resorted
```
