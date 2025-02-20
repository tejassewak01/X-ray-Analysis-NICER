import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
import os

# A obsid directory name can be decomposed in two parts: obsid_constant and obsid_variable.

# EDIT HERE

obsid_constant =  # For example 57060101 is the obsid_constant for a directory 5706010101 and 01 wil be obsid_variable

# There are two options, either give range or directly list out all the obsid_variables
# Here I have listed out all the obsid_variables and commented out the range method. 

#range1, range2 =    # Range for obsid_variable - Example: 1,30

obsid_variables = [] # Note if your variable is 01, just write 1 as padding (01) will be done later

length_of_obsid_variable =     # For example if variable in obsid file is 01,02,03,...30 - then keep length_of_obsid_variable = 2

for obsid_variable in obsid_variables: # CHANGE if using the range method

    obsid_variable = f'{obsid_variable:0{length_of_obsid_variable}}'  # Format obsid_variable as two digits so that 1 is read as 01.

    var = obsid_variable # Change of variable name
    
    mkf_file = f'./{obsid_constant}{var}/auxil/ni{obsid_constant}{var}.mkf'  # Replace with your actual file path
    lc_file_hard = f'./{obsid_constant}{var}/xti/event_cl/ni{obsid_constant}{var}mpu7_sr_hard.lc'  # Hard lightcurve file
    lc_file_soft = f'./{obsid_constant}{var}/xti/event_cl/ni{obsid_constant}{var}mpu7_sr_soft.lc'  # Soft lightcurve file
    lc_file_8to12 = f'./{obsid_constant}{var}/xti/event_cl/ni{obsid_constant}{var}mpu7_sr_8to12.lc'  # 8to12 lightcurve file

    # Open the FITS files
    hdul_mkf = fits.open(mkf_file)
    hdul_lc_hard = fits.open(lc_file_hard)
    hdul_lc_soft = fits.open(lc_file_soft)
    hdul_lc_8to12 = fits.open(lc_file_8to12)

    # Extract data from mkf file
    time_mkf = hdul_mkf[1].data['TIME']
    fpm_count = hdul_mkf[1].data['FPM_OVERONLY_COUNT']
    cor_sax = hdul_mkf[1].data['COR_SAX']

    # Extract data from hard and soft lightcurve files
    time_lc_hard = hdul_lc_hard[1].data['TIME']
    rate_lc_hard = hdul_lc_hard[1].data['RATE']

    time_lc_soft = hdul_lc_soft[1].data['TIME']
    rate_lc_soft = hdul_lc_soft[1].data['RATE']

    rate_lc_8to12 = hdul_lc_8to12[1].data['RATE']

    # Extract GTIs (Good Time Intervals) from hard lightcurve file (assuming GTIs are the same for both)
    gti_start = hdul_lc_hard['GTI'].data['START'] - hdul_lc_hard['GTI'].data['START'][0]
    gti_stop = hdul_lc_hard['GTI'].data['STOP'] - hdul_lc_hard['GTI'].data['START'][0]

    # Filtering valid values
    valid_mkf = np.isfinite(time_mkf) & np.isfinite(fpm_count) & np.isfinite(cor_sax)
    valid_lc_hard = np.isfinite(time_lc_hard) & np.isfinite(rate_lc_hard)
    valid_lc_soft = np.isfinite(time_lc_soft) & np.isfinite(rate_lc_soft)
    valid_lc_8to12 = np.isfinite(time_lc_soft) & np.isfinite(rate_lc_8to12)


    for i, (start, stop) in enumerate(zip(gti_start, gti_stop)):
        # Create masks for GTI intervals for each lc file
        gti_mask_hard = (time_lc_hard >= start) & (time_lc_hard <= stop)
        gti_mask_soft = (time_lc_soft >= start) & (time_lc_soft <= stop)

        # Create a new figure for each GTI with two subplots (one for each lc file)
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

        # Common limits for consistency
        xlim_start, xlim_stop = start, stop # change here HERE.
        #max_y = max(np.nanmax(rate_lc_hard[valid_lc_hard]), np.nanmax(rate_lc_soft[valid_lc_soft]),np.nanmax(rate_lc_8to12[valid_lc_8to12]))
        #ylim_max = max_y + max_y * 0.1  # 10 percent scaling above maximum point

        
        # Plot for 8to12 lightcurve file on the first subplot
        ax1.set_xlim(xlim_start, xlim_stop)
        #ax1.set_ylim(0, ylim_max)
        ax1.plot(time_lc_soft[valid_lc_soft], rate_lc_8to12[valid_lc_8to12], '.', color='blue', label='RATE (8to12 Lightcurve)')
        ax1.plot(time_mkf[valid_mkf] - time_mkf[valid_mkf][0], fpm_count[valid_mkf], 'o', color='orange', label='FPM_OVERONLY_COUNT')
        ax1.plot(time_mkf[valid_mkf] - time_mkf[valid_mkf][0], cor_sax[valid_mkf], '-', color='green', label='COR_SAX')
        ax1.plot(time_mkf[valid_mkf] - time_mkf[valid_mkf][0], 1.5 * np.ones_like(cor_sax[valid_mkf]), '-', color='red', label='COR_SAX_1.5')
        ax1.set_title(f'Electron Flares Check - {obsid_constant}{var} - GTI {i+1} (8to12)')
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Count rate (ct/s)')
        ax1.legend(loc='upper right', prop={'size': 6})
        ax1.grid(True)
        
        # Plot for hard lightcurve file on the second subplot
        ax2.set_xlim(xlim_start, xlim_stop)
        #ax2.set_ylim(0, ylim_max)
        ax2.plot(time_lc_hard[valid_lc_hard], rate_lc_hard[valid_lc_hard], '.', color='blue', label='RATE (Hard Lightcurve)')
        ax2.plot(time_mkf[valid_mkf] - time_mkf[valid_mkf][0], fpm_count[valid_mkf], 'o', color='orange', label='FPM_OVERONLY_COUNT')
        ax2.plot(time_mkf[valid_mkf] - time_mkf[valid_mkf][0], cor_sax[valid_mkf], '-', color='green', label='COR_SAX')
        ax2.plot(time_mkf[valid_mkf] - time_mkf[valid_mkf][0], 1.5 * np.ones_like(cor_sax[valid_mkf]), '-', color='red', label='COR_SAX_1.5')
        ax2.set_title(f'Electron Flares Check - {obsid_constant}{var} - GTI {i+1} (Hard)')
        ax2.set_ylabel('Count rate (ct/s)')
        ax2.legend(loc='upper right', prop={'size': 6})
        ax2.grid(True)
        
        # Plot for soft lightcurve file on the third subplot
        ax3.set_xlim(xlim_start, xlim_stop)
        #ax3.set_ylim(0, ylim_max)
        ax3.plot(time_lc_soft[valid_lc_soft], rate_lc_soft[valid_lc_soft], '.', color='blue', label='RATE (Soft Lightcurve)')
        ax3.plot(time_mkf[valid_mkf] - time_mkf[valid_mkf][0], fpm_count[valid_mkf], 'o', color='orange', label='FPM_OVERONLY_COUNT')
        ax3.plot(time_mkf[valid_mkf] - time_mkf[valid_mkf][0], cor_sax[valid_mkf], '-', color='green', label='COR_SAX')
        ax3.plot(time_mkf[valid_mkf] - time_mkf[valid_mkf][0], 1.5 * np.ones_like(cor_sax[valid_mkf]), '-', color='red', label='COR_SAX_1.5')
        ax3.set_title(f'Electron Flares Check - {obsid_constant}{var} - GTI {i+1} (Soft)')
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Count rate (ct/s)')
        ax3.legend(loc='upper right', prop={'size': 6})
        ax3.grid(True)

        # Save the figure for each GTI
        directory_name = 'pl_electron_flares'
        if not os.path.exists(directory_name):
            # Create the directory if it doesn't exist
            os.makedirs(directory_name)

        output_filename = f'pl_electron_flares/{obsid_constant}{var}_gti{i+1}.png'
        plt.tight_layout()
        plt.savefig(output_filename, format='png', dpi=300)
        print(f"Plot saved as {output_filename}")

        plt.close(fig)  # Close the figure after saving to free memory

    # Close FITS files
    hdul_mkf.close()
    hdul_lc_hard.close()
    hdul_lc_soft.close()

