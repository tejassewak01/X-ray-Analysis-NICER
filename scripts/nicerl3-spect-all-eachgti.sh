#!/bin/sh

# Read each line from list_gti.txt
while IFS= read -r gtifilepath; do
    # Extract GTI number from the filename (digits after 'gti')
    gtinumber=$(echo "$gtifilepath" | grep -oE 'gti[0-9]+' | grep -oE '[0-9]+')

    # Extract obsid (first 10-digit number in the path)
    obsid=$(echo "$gtifilepath" | grep -oE '[0-9]{10}')

    # Run the command
    nicerl3-spect "$obsid" gtifile="$gtifilepath" grouptype=optmin groupscale=25 suffix="_gti$gtinumber" clobber=YES
done < list_gti.txt

