from astropy.io import fits
import numpy as np

# Read file list from txt file
with open("tx_list_gti.txt", "r") as f:
    gti_files = [line.strip() for line in f.readlines()]

# Make a list of all gti_files
gti_files = [file for file in gti_files] # You can also filter out certain directories, by modifying the code line as:
                                         # gti_files = [file for file in gti_files if not file.startswith("5660010601")]

gti_list = []

# Load each GTI file and extract the data
for file in gti_files:
    with fits.open(file) as hdul:
        gti_data = hdul[1].data  # Assuming GTI is in the first extension
        gti_list.append(gti_data)

# Combine all GTI data
if gti_list:
    combined_gti = np.hstack(gti_list)

    # Create a new FITS table with the combined data
    new_hdu = fits.BinTableHDU(data=combined_gti)

    # Save to a new FITS file
    new_hdu.writeto("combined_gti.fits", overwrite=True)

    print("Combined GTI file saved as 'combined_gti.fits'.")
else:
    print("No GTI files left after filtering out.")