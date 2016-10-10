#!/usr/bin/env python 

"""
play tiff file.

Convert all tiff files from a directory into a big numpy array.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2016, Dilawar Singh"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import logging
import cv2

def get_frame_data( frame ):
    try:
        img = np.array(frame)
    except Exception as e:
        img = np.array(frame.convert('L'))
    return to_grayscale(img)

def to_grayscale( img ):
    if len(img.shape) == 3:
        img = np.dot( img[...,:3], [ 0.299, 0.587, 0.114 ] )

    if img.max() >= 256.0:
        logging.debug("Converting image to grayscale")
        logging.debug("Max=%s, min=%s, std=%s"% (img.max(), img.min(),
            img.std()))
        img = 255 * ( img / float( img.max() ))
    gimg = np.array(img, dtype=np.uint8)
    return gimg

def get_bounding_box( ):
    bbox = [ int(x) for x in e.args_.box.split(',') ]
    r1, c1, h, w = bbox

    if h == -1: r2 = h
    else: r2 = r1 + h
    if w == -1: c2 = w
    else: c2 = c1 + w
    return (r1, c1, r2, c2)

def read_frames_from_avi( filename ):
    import cv2
    cap = cv2.VideoCapture( filename )
    frames = []
    while cap.isOpened():
        try:
            ret, frame = cap.read()
        except Exception as e:
            print("Failed to read frame. Error %s" % e)
            quit()
        if ret:
            gray = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY)
            frames.append( gray )

    logging.info("Total %s frames read" % len(frames))
    return frames


def read_frames_from_tiff( filename, **kwargs ):
    from PIL import Image
    tiff = Image.open( filename )
    frames = []
    try:
        i = 0
        while 1:
            i += 1
            tiff.seek( tiff.tell() + 1 )
            framedata = get_frame_data( tiff )
            # bbox = get_bounding_box( )
            # if bbox:
                # framedata = framedata[bbox[0]:bbox[2], bbox[1]:bbox[3]]
            # if kwargs.get('min2zero', False):
                # framedata = framedata - framedata.min()
            frames.append( framedata )
    except EOFError as e:
        logging.info("Total frames read from file %d" % i )
    return frames

def read_frames( videofile, **kwargs ):
    ext = videofile.split('.')[-1]
    if ext in [ 'tif', 'tiff' ]:
        return read_frames_from_tiff( videofile, **kwargs )
    elif ext in [ 'avi', 'mp4' ]:
        return read_frames_from_avi ( videofile, **kwargs )
    else:
        logging.error('Invalid format file %s is not supported yet' % ext )
        quit()

def main( f ):
    frames = read_frames( f )
    for f in frames:
        cv2.imshow( 'frame', f )
        delay = 10
        if len( sys.argv ) > 2:
            delay = int( sys.argv[2] )
        cv2.waitKey( delay )

if __name__ == '__main__':
    tifffile = sys.argv[1]
    main( tifffile )
