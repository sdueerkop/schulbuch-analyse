#!/usr/bin/env python3

######################################
# A script for cropping image files  #
######################################

import os
import subprocess
import logging

from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileMerger

# Logging configuration
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')


def imageCrop(filename,boxTuple):
    myImage = Image.open(filename)
    logging.debug('Opened {}'.format(filename))
    
    width, height = myImage.size
    logging.debug('Image size is: {}x{} pixels'.format(width,height))
    
    croppedImage = myImage.crop(boxTuple)
    logging.debug('Cropped the image.')
    
    croppedImageName = "crp_"+filename
    pdfName = croppedImageName.strip('.jpg')+".pdf"
    #croppedImage.save(croppedImageName)
    #logging.debug('Saved the cropped image {}'.format(croppedImageName))
    croppedImage.save(pdfName, "PDF", resolution=100.0)
    logging.debug('Saved the PDF {}'.format(pdfName))

def ocr(filename):
    # For now uses ocrmypdf
    logging.debug("Beginning OCR of {}".format(filename))
    outputFilename = "ocr_"+filename
    spArguments=["ocrmypdf","-l", "deu", filename, outputFilename]
    subprocess.call(spArguments)

def mergePDF(path):
    # Copied from "Automate the boring stuff"
    logging.debug('Started mergePDF in {}'.format(path))
    folderName = os.path.basename(path)
    outputFile = "StaticOutput.pdf"
    pdfFiles = []
    for filename in os.listdir(path):
        if (filename.endswith('.pdf') and filename.startswith('ocr_')):
            pdfFiles.append(filename)
    pdfFiles.sort(key=str.lower)
    
    merger = PdfFileMerger()
    for filename in pdfFiles:
        merger.append(PdfFileReader(os.path.join(path, filename), "rb"))
    merger.write(os.path.join(path, outputFile))

def cleanUp(path):
    # Cleaning up the files produced by the other functions
    for f in os.listdir(path):
        if (f.endswith('.pdf') and (f.startswith('crp_') or f.startswith('ocr_'))):
            os.unlink(f)
            logging.debug('Deleting file {}'.format(f))

if __name__ == "__main__":

    srcDir ='/home/sven/.temp/imageCropping/Spinner2012_Wie_Fachwissen_das_literarische_Verstaendnis_stoert/'
    os.chdir(srcDir)
    
    # Crop images in a directory and store them as JPEG and PDF
    for img in os.listdir(srcDir):

        # Check for non-image files
        if not (img.endswith('.png') or img.endswith('.jpg') ):
            continue
        # Check for files already cropped
        elif img.startswith('crp_'):
            continue

        filename = img
        boxTuple = (0,0,1758,2463)
        imageCrop(filename,boxTuple)
        print("\n")

    for pdf in os.listdir(srcDir):
        if not (pdf.endswith('.pdf')):
            continue
        logging.debug("Filename is {}".format(pdf))        
#        filename = pdf
#        ocr(filename)
    
    # Merge PDFs
#    mergePDF(srcDir)
    # Clean up temporary files
    #cleanUp(srcDir)
