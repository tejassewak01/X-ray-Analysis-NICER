#!/bin/bash

# Loop through all 10-digit directories in the current directory
for obsid in [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]; do
    # Check if it's a directory
    if [[ -d "$obsid" ]]; then
        # Look for GTI files in the expected directory structure
        for gti_file in "$obsid/xti/event_cl/gti"*.fits; do
            # Check if the GTI file exists
            if [[ -f "$gti_file" ]]; then
                echo "$gti_file" >> tx_list_gti.txt
                echo "Added: $gti_file"  # Print which file was added
            fi
        done
    fi
done

echo "Done."

