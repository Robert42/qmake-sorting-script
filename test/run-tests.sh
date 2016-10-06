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

echo '# move inl files from SOURCES to HEADERS
SOURCES = \
    aaa.cpp \
    bbb.cpp \
    bbb.inl \
    ccc.inl
SOURCES += \
    ddd.cpp \
    eee.cpp \
    eee.inl \
    fff.cpp
HEADERS = u.h v.inl w.h
HEADERS += x.inl y.h z.h
' > test7.pro

echo '# move inl files from HEADERS to SOURCES
SOURCES = \
    aaa.cpp \
    bbb.cpp \
    bbb.inl \
    ccc.inl
SOURCES += \
    ddd.cpp \
    eee.cpp \
    eee.inl \
    fff.cpp
HEADERS = u.h v.inl w.h
HEADERS += x.inl y.h z.h
' > test8.pro

echo '# move inl files from SOURCES to not existing HEADERS
SOURCES = \
    aaa.cpp \
    bbb.cpp \
    bbb.inl \
    ccc.inl
SOURCES += \
    ddd.cpp \
    eee.cpp \
    eee.inl \
    fff.inl
' > test9.pro

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

echo '# move inl files from SOURCES to HEADERS
SOURCES = \
    aaa.cpp \
    bbb.cpp
SOURCES += \
    ddd.cpp \
    eee.cpp \
    fff.cpp
HEADERS = \
    u.h \
    v.inl \
    w.h
HEADERS += \
    bbb.inl \
    ccc.inl \
    eee.inl \
    x.inl \
    y.h \
    z.h
' > expected7.pro

echo '# move inl files from HEADERS to SOURCES
SOURCES = \
    aaa.cpp \
    bbb.cpp \
    bbb.inl \
    ccc.inl
SOURCES += \
    ddd.cpp \
    eee.cpp \
    eee.inl \
    fff.cpp \
    v.inl \
    x.inl
HEADERS = \
    u.h \
    w.h
HEADERS += \
    y.h \
    z.h
' > expected8.pro

echo '# move inl files from SOURCES to not existing HEADERS
SOURCES = \
    aaa.cpp \
    bbb.cpp
SOURCES += \
    ddd.cpp \
    eee.cpp

HEADERS = \
    bbb.inl \
    ccc.inl \
    eee.inl \
    fff.inl' > expected9.pro

compare_with_expected()
{
  diff test1.pro expected1.pro
  diff test2.pro expected2.pro
  diff test3.pro expected3.pro
  diff test4.pro expected4.pro
  diff test5.pro expected5.pro
  diff test6.pro expected6.pro
  diff test7.pro expected7.pro
  diff test8.pro expected8.pro
  diff test9.pro expected9.pro
}


run_script()
{
  $SCRIPT $1 --files test1.pro test2.pro test3.pro test4.pro test5.pro test6.pro
  $SCRIPT $1 --move-inl-to-headers --files test7.pro test9.pro
  $SCRIPT $1 --move-inl-to-sources --files test8.pro
}

run_script

compare_with_expected

run_script --print-resorted-files

compare_with_expected

