#! /bin/bash

DIR=$(dirname $(readlink -f $0))
TEST_DIR=$DIR/test-files

rm -rf $TEST_DIR
mkdir $TEST_DIR

cd $TEST_DIR

echo '
SOURCES += bbb ccc aaa
CONFIG= x y z
' > test1.pro

echo '
SOURCES+=\
bbb ccc aaa
CONFIG= x y z
' > test2.pro

echo '
SOURCES+=\
bbb\
ccc \
aaa
CONFIG= x y z
' > test3.pro

echo '
SOURCES+=bbb \
ccc \
aaa
CONFIG= x y z
' > test4.pro

echo '
SOURCES+=ddd aaa \
bbb fff \
eee ccc
CONFIG= x y z
' > test5.pro

echo '
SOURCES+=bbb \
\
ccc \
\
aaa \
\

CONFIG= x y z
' > test6.pro


