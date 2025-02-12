import astropy.io.fits as fits
import numpy as np

# RUNNING THIS CELL WILL REMOVE UNCOMBINED GTI FILES, IF YOU DO NOT WANT TO DELETE THESE FILES,
# COMMENT OUT LAST BIT OF CODE

# List of GTI file numbers you want to combine
obsid_constant =    # Not a string
obsid_variable =    # Say for example i want to combine two gti files 1 and 2 in obsid 10. Then
gtinumbers = []     # List of gtinumbers to combine, for above example, the list is [1,2]

# Construct the file paths based on the file numbers
gti_files = [f"./{obsid_constant}{obsid_variable}/xti/event_cl/gti{gtinumber}.fits" for gtinumber in gtinumbers]
# Initialize an empty list to hold GTI data
gti_data = []
# Loop over each file, load the data, and append to the list
for file in gti_files:
    with fits.open(file) as hdul:
        gti_data.append(hdul[1].data)
# Concatenate all GTI data into a single table
combined_gti_data = np.concatenate(gti_data)
print(combined_gti_data)

# Create a new HDU with the combined data
hdu = fits.BinTableHDU(data=combined_gti_data)
# Construct the output filename based on the file numbers
output_filename = f"./{obsid_constant}{obsid_variable}/xti/event_cl/gti" + "".join(map(str, gtinumbers)) + ".fits"
# Write to a new FITS file
hdu.writeto(output_filename, overwrite=True)
print("GTI file saved as:", output_filename)

# Choose to delete the original (uncombined) gti files

import os

# Iterate through the list of GTI file paths and remove them
for file_path in gti_files:
    if os.path.exists(file_path):  # Check if the file exists
        os.remove(file_path)  # Remove the file
        print(f"File {file_path} removed.")
