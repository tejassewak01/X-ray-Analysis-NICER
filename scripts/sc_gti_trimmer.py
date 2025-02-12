from astropy.io import fits
import numpy as np

obsid_constant = __ "Constant part of obsid"
obsid_variable = __ "Variable part of obsid"
gtinumber = __      "gtinumber which you want to trim"

length_of_obsid_variable =  _   # For example if variable in obsid file is 01,02,03,...30 - then keep length_of_obsid_variable = 2
                                # if variable in obsid file is 101,102,103...150 - then keep length_of_obsid_variable = 3
    
obsid_variable = f'{obsid_variable:0{length_of_obsid_variable}}'  # Format obsid_variable as two digits so that 1 is read as 01.

# Path to the GTI file
gti_file = f'./{obsid_constant}{obsid_variable}/xti/event_cl/gti{gtinumber}.fits'

# Trim values
add_start = 0  # The amount of time you want to add to the START
sub_stop =  0   # The amount of time you want to subtract from the STOP

# Open the GTI file in 'update' mode
with fits.open(gti_file, mode='update') as hdul:
    gti_data = hdul[1].data  # Access the GTI extension (typically at index 1)
    
    # Check the original values
    print(f"Original START: {gti_data['START'][0]}")
    print(f"Original STOP: {gti_data['STOP'][0]}")

    new_start = gti_data['START'][0] + add_start
    new_stop  = gti_data['STOP'][0]  - sub_stop 

    
    # Update the START and STOP values
    gti_data['START'][0] = new_start
    gti_data['STOP'][0] = new_stop

    # Save changes to the FITS file
    hdul.flush()  # Ensures changes are written to the file

# Print confirmation
print(f"Updated START: {gti_data['START'][0]}")
print(f"Updated STOP: {gti_data['STOP'][0]}")
print("GTI file updated successfully.")

