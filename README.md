# Order Optimizer
OpenCV &amp; PySerial driven order optimizer for kitchen staff.

This optimizer simplifies the food preperation process in a line kitchen.  Chefs are able to reference a single queue rather than parsing large groups of paper tickets to determine what needs to be prepared.  This greatly reduces the cost of wasted product due to preperation errors while simultaneously increasing the rate of output per kitchen staff.

RS232 communications are sampled from a twisted-pair network cable connecting an Epson TM-T88VI thermal printer to a network hosting ALOHA Point of Sale software.  These communications are translated to 3.3V TTL logic levels compatible with Raspberry Pi 4B using a MAX3232 IC.  Parsing the ESC/POS (https://reference.epson-biz.com/modules/ref_escpos/index.php?content_id=2) bytestring is fully software driven in Python.

## Usage
Target 'main.py'; use option '--sim_serial' to simulate serial receive data with tickets in ticket_samples directory.

Ex: 'python3 main.py' OR 'python3 main.py --sim_serial'

## Additional Package Requirements
PySerial - https://github.com/pyserial/pyserial -- with pip, use 'pip install pyserial'

OpenCV - https://opencv.org/ -- with pip, use 'pip install opencv-python'
*Full binaries are not required*

NumPy - https://numpy.org/ -- with pip, use 'pip install numpy'

## Quick Video about Development Process
https://www.youtube.com/watch?v=qYPLYr8YbpQ
