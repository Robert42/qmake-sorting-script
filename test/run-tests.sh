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

echo '# handle all in the first line
SOURCES += \
    aaa \
    bbb \
    ccc
CONFIG= x y z
' > expected1.pro

echo '# handle all in the second line
SOURCES += \
    aaa \
    bbb \
    ccc
CONFIG= x y z
' > expected2.pro

echo '# handle first line empty
SOURCES += \
    aaa \
    bbb \
    ccc
CONFIG= x y z
' > expected3.pro

echo '# handle first line non empty
SOURCES += \
    aaa \
    bbb \
    ccc
CONFIG= x y z
' > expected4.pro

echo '# handle multiple per line
SOURCES += \
    aaa \
    bbb \
    ccc \
    ddd \
    eee \
    fff
CONFIG= x y z
' > expected5.pro

echo '# handle empty following lines
SOURCES += \
    aaa \
    bbb \
    ccc
CONFIG= x y z
' > expected6.pro

compare_with_expected()
{
  diff test1.pro expected1.pro
  diff test2.pro expected2.pro
  diff test3.pro expected3.pro
  diff test4.pro expected4.pro
  diff test5.pro expected5.pro
  diff test6.pro expected6.pro
}

RUN_SCRIPT="$SCRIPT --files test1.pro test2.pro test3.pro test4.pro test5.pro test6.pro"

$RUN_SCRIPT

compare_with_expected

