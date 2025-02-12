#!/bin/sh
for obsid in [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]; do
 nicerl3-lc $obsid pirange=30-200 timebin=60.0 suffix=_soft clobber=YES
 nicerl3-lc $obsid pirange=200-800 timebin=60.0 suffix=_hard clobber=YES
 nicerl3-lc $obsid pirange=800-1200 timebin=60.0 suffix=_8to12 clobber=YES
done
