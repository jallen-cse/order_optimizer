import numpy as np
from copy import deepcopy, copy
import pytesseract 
from pytesseract import Output      #redundant

from optimizer import *
from cv2_ui import *

def UIMouseCallback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_LBUTTONDBLCLK:
        for panel in ui_shown_panels:
            if x > panel.x_pos and x < panel.x_pos2 and y > panel.y_pos and y < panel.y_pos2:
                for element in panel.elements:
                    if x > element.x_pos and x < element.x_pos2 and y > element.y_pos and y < element.y_pos2:
                        if isinstance(element, Button):
                            element.callback(element.text)

def QueueMouseCallback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_LBUTTONDBLCLK:
        for element in queue_control_panel.elements:
            if x > element.x_pos and x < element.x_pos2 and y > element.y_pos and y < element.y_pos2:
                if isinstance(element, Button):
                    element.callback(element.text)

def buttonCallback(text):
    print(text)
    
    global state
    state = text

    global ui_shown_panels
    
    if text == "Beverages":
        ui_shown_panels = set((category_panel, beverage_panel))
    elif text == "Appetizers":
        ui_shown_panels = set((category_panel, appetizer_panel))
    elif text == "Pitas & Wraps":
        ui_shown_panels = set((category_panel, pitas_panel))
    elif text == "Desserts":
        ui_shown_panels = set((category_panel, dessert_panel))
    elif text == "Beer & Wine":
        ui_shown_panels = set((category_panel, beer_panel))

    else:
        optimizer.add(ListItem(text, 1))

def queueButtonCallback(text):
    if text == "plus":
        queue_pop_counter.increment(1)
    elif text == "minus":
        queue_pop_counter.increment(-1)
    elif text == "up_arrow":
        optimizer.incrementCursor(-1)
    elif text == "down_arrow":
        optimizer.incrementCursor(1)
    elif text == "DONE":
        optimizer.remove(ListItem(optimizer.item_queue[optimizer.cursor].text, queue_pop_counter.val))
        queue_pop_counter.increment(-queue_pop_counter.val)


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def crappy_abs_func(val):
    if val < -45:
        return val + 90
    return val

def prettyData(data):
    lines = {}

    for n in range(len(data['text'])):
        if data['text'][n] in item_set:            
            try:
                lines[data['line_num'][n]]['words'].append(data['text'][n])
            except KeyError:
                lines[data['line_num'][n]] = {'words' : [data['text'][n]], 'left' : data['left'][n], 'quantity' : 1}
                
                try:
                    lines[data['line_num'][n]]['quantity'] = int(data['text'][n-1])
                    lines[data['line_num'][n]]['left'] = data['left'][n-1]
                except ValueError:
                    pass
    return lines

def itemizeRecogData(data):
    print(data)

    lines = {}
    quantities = {}
    items = []

    left_margin = 0

    for n in range(len(data['text'])):
        if data['text'][n] in item_set:
            print(str(data['left'][n]) + " " + data['text'][n])
            
            try:
                lines[data['line_num'][n]].append(data['text'][n])
            except KeyError:
                lines[data['line_num'][n]] = [data['text'][n]]
                
                try:
                    quantities[data['line_num'][n]] = int(data['text'][n-1])
                except ValueError:
                    quantities[data['line_num'][n]] = 1
        

    for line in lines:
        concat = ""
        
        for word in lines[line]:
            concat += word + " "

        items.append(ListItem(concat, quantities[line]))

    parsed_items = []

    
    return items

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
item_set = set(["Shawarma", "Pita", "Chicken", "Combo", "SM", "Hummus", "Gyro", "Philly", "Chkn", "ChKn", "WF", "Salmon", "LG", "Greek", "Salad", "&", "NO", "Pita", "Pitas", "SUB", "Cucumber"])

queue_canvas_width = 325
queue_canvas_height = 600

queue_canvas = np.ones((queue_canvas_height, queue_canvas_width, 3), np.uint8)

#OPENCV UI COMPONENTS
queue_control_panel = Panel("Queue Control Panel", 0, 435, 325, 165, (0, 50, 0))

up_arrow = cv2.imread("C:/Users/Owner/OneDrive/Documents/Projects/Python Order Optimization/gui/textures/up_arrow.png")
down_arrow = cv2.imread("C:/Users/Owner/OneDrive/Documents/Projects/Python Order Optimization/gui/textures/down_arrow.png")
plus_sign = cv2.imread("C:/Users/Owner/OneDrive/Documents/Projects/Python Order Optimization/gui/textures/plus.png")
minus_sign = cv2.imread("C:/Users/Owner/OneDrive/Documents/Projects/Python Order Optimization/gui/textures/minus.png")

queue_pop_counter = Counter(0, 20001, 5, 5, 75, 75, text_color = (255, 255, 255))

queue_control_panel.addElement(Button("up_arrow", 10001, x_pos = 245, y_pos = 5, width = 75, height = 75, texture = up_arrow))
queue_control_panel.addElement(Button("down_arrow", 10001, x_pos = 245, y_pos = 85, width = 75, height = 75, texture = down_arrow))
queue_control_panel.addElement(Button("plus", 10001, x_pos = 165, y_pos = 5, width = 75, height = 75, texture = plus_sign))
queue_control_panel.addElement(Button("minus", 10001, x_pos = 85, y_pos = 5, width = 75, height = 75, texture = minus_sign))
queue_control_panel.addElement(Button("DONE", 10001, x_pos = 5, y_pos = 85, width = 235, height = 75, color = (0, 0, 0), text_color = (255, 255, 255)))
queue_control_panel.addElement(queue_pop_counter)

for element in queue_control_panel.elements:
    if isinstance(element, Button):
        element.addCallback(queueButtonCallback)

#create UI window
cv2.namedWindow("ORDER QUEUE", cv2.WINDOW_GUI_EXPANDED)
cv2.namedWindow("frame", cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback("ORDER QUEUE", QueueMouseCallback)

#create video capture object from webcam -> using native iPhone HD, works with other res
cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)

#create an optimizer
optimizer = OrderOptimizer()

loop_count = 0
valid_arcmax = 0

#main UI loop
while True:
    queue_frame = copy(queue_canvas)
    
    queue_control_panel.drawSelf(queue_frame)

    optimizer.drawSelf(queue_frame)

    cv2.imshow("ORDER QUEUE", queue_frame)
    key = cv2.waitKey(33)

    #text recognition section

    if not loop_count % 3:
        _, frame = cap.read()

        #img processing done here, more might be wanted
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 200, 255, 0)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        arcmax = None

        for contour in contours:
            if arcmax is not None:
                arcmax = contour if cv2.arcLength(contour, False) > cv2.arcLength(arcmax, False) else arcmax
            else:
                arcmax = contour
        
        if arcmax is not None:
            x, y, w, h = cv2.boundingRect(arcmax)

            rot_rect = cv2.minAreaRect(arcmax)
            cropped_frame = frame[y:y+h, x:x+w]


            if cv2.contourArea(arcmax) > 500000:

                valid_arcmax += 1

                if valid_arcmax == 16:
                    cv2.drawContours(frame, [arcmax], 0, (0, 255, 0), 5)

                    center = (w//2, h//2)
                    M = cv2.getRotationMatrix2D(center, crappy_abs_func(rot_rect[2]), 1)
                    rotated_cropped_frame = cv2.warpAffine(cropped_frame, M, (w, h))

                    cropped_bin_frame = thresh[y:y+h, x:x+w]
                    rotated_cropped_bin_frame = cv2.warpAffine(cropped_bin_frame, M, (w, h))

                    cv2.imshow('frame', rotated_cropped_bin_frame)
                    cv2.waitKey(1000)

                    recog_data = pytesseract.image_to_data(rotated_cropped_bin_frame, output_type=Output.DICT)

                    items = itemizeRecogData(recog_data)
                    print("PRETTY : \n" + str(prettyData(recog_data)))

                    for item in items:
                        optimizer.add(item)

                    valid_arcmax = 0
                else:
                    cv2.drawContours(frame, [arcmax], 0, (0, 255, 255), 5)
                    cv2.imshow('frame', cropped_frame)
                    #cv2.waitKey(100)
            else:
                valid_arcmax = 0
                cv2.imshow('frame', cropped_frame)
                #cv2.waitKey(100)

        loop_count = 0

    if key == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

    loop_count += 1
