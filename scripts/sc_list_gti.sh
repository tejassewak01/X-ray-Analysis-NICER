#!/bin/bash

# Loop through obsid directories, where each obsid is a 10-digit number
for obsid in {0000000000..9999999999}; do
    # Look for GTI files in the specific directory structure
    for gti_file in "./${obsid}/xti/event_cl/gti*.fits"; do
        # Check if the GTI file exists and append its path to list_gti.txt
        if [[ -f "$gti_file" ]]; then
            echo "$gti_file" >> list_gti.txt
        fi
    done
done

# Print a message when done
echo "GTI files have been appended to list_gti.txt."
