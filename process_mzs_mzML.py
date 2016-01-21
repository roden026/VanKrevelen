'''
Churns through an mzML object to generate lists of positive and negative
mz values.

pymzml citation
Bald, T., Barth, J., Niehues, A., Specht, M., Hippler, M., and Fufezan, C. (2012) pymzML - Python module for high throughput bioinformatics on mass spectrometry data, Bioinformatics, doi: 10.1093/bioinformatics/bts066
'''

import pymzml
import sys

# What fraction of the max intensity you want to use for a threshold
THRESHOLD_CONSTANT = .1


# Takes an mzXML object which contains a list of intensities, a
# list of mzs, and a value for the threshold intensity for filtering.
def process_mzs(file_name):

    # Sets up mzML reader
    ms_run = pymzml.run.Reader(
        file_name,
        obo_version='1.1.0',
        extraAccessions=[
            ('MS:1000129', ['value']),
            ('MS:1000130', ['value'])
        ]
    )

    # For elements that clear the filter
    keepers_neg_mz = []
    keepers_pos_mz = []

    '''
    Loops through positive list and negative list and adds mz values to the keeper list when the intensity is
    above a threshold and catches any errors that are thrown (test data still had some issues with encoded data
    not decoding properly but the try and except handles that).
    '''
    # Variable to make sure loop continues even if an error is thrown
    running = True
    while running:
        try:
            i = 0
            # for each spectrum in a "run" (iteration)
            for spectrum in ms_run:

                # Calculate the max value and then generate a threshold based on that.
                maxS = max(spectrum.i)
                thresh = maxS * THRESHOLD_CONSTANT

                # Looks at each peak intensity, and if it is past the thresh hold, adds it to the neg or pos list
                for peak in spectrum.peaks:
                    if peak[1] > thresh:
                        negative_polarity = spectrum.get('MS:1000129', False)
                        if negative_polarity == '':
                            keepers_neg_mz.append(peak[0])

                        positive_polarity = spectrum.get('MS:1000130', False)
                        if positive_polarity == '':
                            keepers_pos_mz.append(peak[0])

            running = False

        # Error catching. Generic used here for readability
        except:
            pass

    # Removes duplicates
    filtered_neg_mz = list(set(keepers_neg_mz))
    filtered_pos_mz = list(set(keepers_pos_mz))

    # Combines list where negatives are in the 0 position and positives in the 1
    combo_set = [filtered_neg_mz, filtered_pos_mz]
    return combo_set


