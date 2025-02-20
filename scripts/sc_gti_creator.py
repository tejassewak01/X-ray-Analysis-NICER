from astropy.io import fits
import numpy as np

# A obsid directory name can be decomposed in two parts: obsid_constant and obsid_variable./

obsid_constant = 566001  # For example 57060101 is the obsid_constant for a directory 5706010101 and 01 wil be obsid_variable


# Now, there are two options, either give range or directly list out all the obsid_variables
# Here I have listed out all the obsid_variables and commented out the range method. 

#range1, range2 =    # Range for obsid_variable - Example: 1,30

obsid_variables = [] # Note if your variable is 01, just write 1 as padding (01) will be done later. 
#Example list [1,2,3,4,5,6,7,8,9,10,11,...30]. Helpful if example list is like [101,201,301,401,501,601,701,801,901,1001,1101,1201,...3001]

length_of_obsid_variable =     # For example if variable in obsid file is 01,02,03,...30 - then keep length_of_obsid_variable = 2

for obsid_variable in obsid_variables: # CHANGE if using the range method

    obsid_variable = f'{obsid_variable:0{length_of_obsid_variable}}'  # Format obsid_variable as two digits so that 1 is read as 01.

    # File paths (adjust as necessary)
    lc_file = f'./{obsid_constant}{obsid_variable}/xti/event_cl/ni{obsid_constant}{obsid_variable}mpu7_sr_soft.lc'  # Choose any one of lightcurve file

    # Open the FITS files
    hdul_lc = fits.open(lc_file)

    # Extract GTIs (Good Time Intervals) from the lightcurve file
    gti_start = hdul_lc['GTI'].data['START']
    gti_stop = hdul_lc['GTI'].data['STOP']

    # Loop over each GTI start-stop pair and create a new FITS file
    for i, (start, stop) in enumerate(zip(gti_start, gti_stop)):
 
       # Create a new HDU (Header/Data Unit) for the GTI file
        col1 = fits.Column(name='START', format='D', array=np.array([start]))
        col2 = fits.Column(name='STOP', format='D', array=np.array([stop]))
        hdu = fits.BinTableHDU.from_columns([col1, col2])

        #Write the GTI to a new FITS file
        gti_filename = f'{obsid_constant}{obsid_variable}/xti/event_cl/gti{i + 1}.fits'
        hdu.writeto(gti_filename, overwrite=True)

        print(f"GTI file created: {gti_filename}")

    # Close the FITS files
    hdul_lc.close()
