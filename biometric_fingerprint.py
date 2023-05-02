#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import tempfile
from pyfingerprint.pyfingerprint import PyFingerprint


## Tries to initialize the sensor
def fingerprint():
    try:
        # Attempt to initialize the fingerprint sensor
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            # if value is wrong, capture a snapshot
            print('Downloading image (this take a while)...')
            imageDestination =  tempfile.gettempdir() + '/fingerprint.bmp'
            f.downloadImage(imageDestination)
            print('The image was saved to "' + imageDestination + '".')
            
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)
    
    # Get and print some sensor information
    print('Currently used templates: ' + str(f.getTemplateCount()) + '/' + str(f.getStorageCapacity()))

    # Attempt to search for the fingerprint and calculate its hash
    try:
        # Prompt the user to place their finger on the sensor
        print('Waiting for finger...')

        # Wait until the finger is read
        while (f.readImage() == False):
            pass

        # Convert the read image to characteristics and store it in charbuffer 1
        f.convertImage(0x01)

        # Search for a matching template in the sensor's database
        result = f.searchTemplate()

        # Extract the position number and accuracy score from the result
        positionNumber = result[0]
        accuracyScore = result[1]

        # If no match is found, print a message and exit
        if (positionNumber == -1):
            print('No match found!')
            exit(0)
        else:
            # If a match is found, print the position number and accuracy score
            print('Found template at position #' + str(positionNumber))
            print('The accuracy score is: ' + str(accuracyScore))

        # Load the found template into charbuffer 1
        f.loadTemplate(positionNumber, 0x01)

        # Download the characteristics of the template loaded in charbuffer 1
        characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

        # Hash the characteristics of the template using SHA-256
        print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())
        return positionNumber

    except Exception as e:
        # Print an error message if the operation fails
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)