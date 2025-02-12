#!/bin/sh

# Read each line from list_gti.txt
while IFS= read -r gtifilepath; do
    # Extract GTI number from the filename (digits after 'gti')
    gtinumber=$(echo "$gtifilepath" | grep -oE 'gti[0-9]+' | grep -oE '[0-9]+')

    # Extract obsid (first 10-digit number in the path)
    obsid=$(echo "$gtifilepath" | grep -oE '[0-9]{10}')

    # Run the command
    nicerl3-lc "$obsid" gtifile="$gtifilepath" pirange=30-200 timebin=60.0 suffix="_soft_gti$gtinumber" clobber=YES
    nicerl3-lc "$obsid" gtifile="$gtifilepath" pirange=200-800 timebin=60.0 suffix="_hard_gti$gtinumber" clobber=YES
    nicerl3-lc "$obsid" gtifile="$gtifilepath" pirange=800-1200 timebin=60.0 suffix="_8to12_gti$gtinumber" clobber=YES
done < list_gti.txt
