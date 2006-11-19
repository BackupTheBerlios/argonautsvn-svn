#!/bin/sh

sudo ./setup.py install

if [ ! -d /tmp/asvn-test ]
then
    mkdir /tmp/asvn-test
fi
export TMPDIR=/tmp/asvn-test

nautilus --no-desktop .