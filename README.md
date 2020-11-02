# Order Optimizer
OpenCV &amp; PyTesseract driven order optimizer for kitchen staff.

This optimizer simplifies the food preperation process in a line kitchen.  Chefs are able to reference a single queue rather than parsing dozens of paper tickets to determine what needs to be sold.  This greatly reduces the cost of wasted product due to preperation errors while increasing the rate of output per kitchen staff.

## Requirements
PyTesseract - https://github.com/madmaze/pytesseract
-- note this also requires tesseract OCR binaries be installed locally.  Define the path to these binaries on line 124 of main.py.

OpenCV - https://opencv.org/ -- with pip, use 'pip install opencv-python'

NumPy - https://numpy.org/ -- with pip, use 'pip install numpy'
