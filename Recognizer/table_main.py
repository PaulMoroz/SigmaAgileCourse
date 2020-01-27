import numpy as np
import cv2 as cv
import utils
from table import Table
from PIL import Image
import sys

# =====================================================
# IMAGE LOADING
# =====================================================		
def find_table(image):
	# Convert resized RGB image to grayscale
	NUM_CHANNELS = 3
	if len(image.shape) == NUM_CHANNELS:
	    grayscale = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

	# =====================================================
	# IMAGE FILTERING (using adaptive thresholding)
	# =====================================================
	MAX_THRESHOLD_VALUE = 255
	BLOCK_SIZE = 15
	THRESHOLD_CONSTANT = 0

	# Filter image
	filtered = cv.adaptiveThreshold(~grayscale, MAX_THRESHOLD_VALUE, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, BLOCK_SIZE, THRESHOLD_CONSTANT)
 
	# =====================================================
	# LINE ISOLATION
	# =====================================================
	SCALE = 15

	# Isolate horizontal and vertical lines using morphological operations
	horizontal = filtered.copy()
	vertical = filtered.copy()

	horizontal_size = int(horizontal.shape[1] / SCALE)
	horizontal_structure = cv.getStructuringElement(cv.MORPH_RECT, (horizontal_size, 1))
	utils.isolate_lines(horizontal, horizontal_structure)

	vertical_size = int(vertical.shape[0] / SCALE)
	vertical_structure = cv.getStructuringElement(cv.MORPH_RECT, (1, vertical_size))
	utils.isolate_lines(vertical, vertical_structure)

	# =====================================================
	# TABLE EXTRACTION
	# =====================================================
	# Create an image mask with just the horizontal
	# and vertical lines in the image. Then find
	# all contours in the mask.
	mask = horizontal + vertical
	(contours, _) = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

	# Find intersections between the lines
	# to determine if the intersections are table joints.
	intersections = cv.bitwise_and(horizontal, vertical)

	# Get tables from the images
	tables = [] # list of tables
	for i in range(len(contours)):
	    # Verify that region of interest is a table
	    (rect, table_joints) = utils.verify_table(contours[i], intersections)
	    if rect == None or table_joints == None:
	        continue

	    # Create a new instance of a table
	    table = Table(rect[0], rect[1], rect[2], rect[3])

	    # Get an n-dimensional array of the coordinates of the table joints
	    joint_coords = []
	    for i in range(len(table_joints)):
	        joint_coords.append(table_joints[i][0][0])
	    joint_coords = np.asarray(joint_coords)

	    # Returns indices of coordinates in sorted order
	    # Sorts based on parameters (aka keys) starting from the last parameter, then second-to-last, etc
	    sorted_indices = np.lexsort((joint_coords[:, 0], joint_coords[:, 1]))
	    joint_coords = joint_coords[sorted_indices]

	    # Store joint coordinates in the table instance
	    table.set_joints(joint_coords)

	    tables.append(table)
	if len(tables)!=0:
	    return tables
	else:
		return None
    

