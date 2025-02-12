#!/bin/sh
for obsid in [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]; do
  nicerl2 indir=$obsid clobber=YES
done

