#! /bin/bash

DIR=$(dirname $(readlink -f $0))
TEST_DIR=$DIR/test-files
SCRIPT=$DIR/../qmake-sorting-script.py


rm -rf $TEST_DIR
mkdir $TEST_DIR

cd $TEST_DIR

echo '# handle all in the first line
SOURCES += bbb ccc aaa
CONFIG= x y z
' > test1.pro

echo '# handle all in the second line
SOURCES+=\
bbb ccc aaa
CONFIG= x y z
' > test2.pro

echo '# handle first line empty
SOURCES+=\
bbb\
ccc \
aaa
CONFIG= x y z
' > test3.pro

echo '# handle first line non empty
SOURCES+=bbb \
ccc \
aaa
CONFIG= x y z
' > test4.pro

echo '# handle multiple per line
SOURCES+=ddd aaa \
bbb fff \
eee ccc
CONFIG= x y z
' > test5.pro

echo '# handle empty following lines
SOURCES+=bbb \
\
ccc \
\
aaa \
\

CONFIG= x y z
' > test6.pro

RUN_SCRIPT=$SCRIPT --files test1.pro test2.pro test3.pro test4.pro test5.pro test6.pro

$RUN_SCRIPT

