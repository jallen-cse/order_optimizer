# Order Optimizer
OpenCV &amp; PySerial driven order optimizer for kitchen staff.

This optimizer simplifies the food preperation process in a line kitchen.  Chefs are able to reference a single queue rather than parsing large groups of paper tickets to determine what needs to be prepared.  This greatly reduces the cost of wasted product due to preperation errors while simultaneously increasing the rate of output per kitchen staff.

RS323 communications are sampled from a twisted-pair network cable connecting an Epson TM-T88VI thermal printer to network hosting ALOHA Point of Sale software.  These communications are translated to 3.3V TTL logic levels compatible with Raspberry Pi 4B using a MAX3232 IC.  Parsing the ESC/POS (https://reference.epson-biz.com/modules/ref_escpos/index.php?content_id=2) bytestring is fully software driven by Python.

## Requirements
PySerial - https://github.com/pyserial/pyserial -- with pip, use 'pip install pyserial'

OpenCV - https://opencv.org/ -- with pip, use 'pip install opencv-python'

NumPy - https://numpy.org/ -- with pip, use 'pip install numpy'
