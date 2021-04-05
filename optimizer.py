import cv2
import time

#########################
#   Optimizer Classes   #
#########################

class ListItem:
    def __init__(self, text, quantity):
        self.text = text
        self.quantity = quantity
        self.time_list = []
        self.time = time.time()
    
    def __hash__(self):
        return hash(self.text)

    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.time < other.time

    def __str__(self):
        return str(self.quantity) + " " + self.text + " " + str(int(time.time() - self.time))

class Order:
    def __init__(self, ID, guests):
        self.ID = ID
        self.guests = guests
        self.time = time.time()

class OrderOptimizer:
    def __init__(self, name):
        self.name = name
        self.order_queue = []
        self.item_queue = []
        self.item_set = set()

        self.cursor = 0

    def __eq__(self, other):
        return self.name == other.name

    def justify(self, top_left):
        self.left_justification = top_left[0]
        self.top_justification = top_left[1]

    def add(self, item):
        if item not in self.item_set:
            self.item_set.add(item)
            self.item_queue.append(item)

            for n in range(item.quantity):
                item.time_list.append(item.time)

        else:
            for queued_item in self.item_queue:
                if queued_item == item:
                    queued_item.quantity += item.quantity
                    
                    for each in range(item.quantity):
                        queued_item.time_list.append(item.time)

    def remove(self, item):
        if item in self.item_set:
            for queued_item in self.item_queue:
                if queued_item == item:
                    if queued_item.quantity > item.quantity:
                        queued_item.quantity -= item.quantity

                        for n in range(item.quantity):
                            queued_item.time_list.pop(0)

                        queued_item.time = queued_item.time_list[0]

                        self.reSort()

                        #linear search to relocate cursor, OK because n very small
                        for i, itm in enumerate(self.item_queue):
                            if item == itm:
                                self.cursor = i
                    else:
                        self.item_queue.remove(queued_item)
                        self.item_set.remove(queued_item)
                        self.reSort()
                        self.incrementCursor(-self.cursor)
                    
                    return

    def reSort(self):
        self.item_queue.sort()
        self.incrementCursor(0)

    #Unused as of now -> to support future features
    def attachCursor(self, _cursor):
        self.cursor = _cursor

    def incrementCursor(self, val):
        if len(self.item_queue):
            self.cursor = (self.cursor + val) % len(self.item_queue)
        else:
            self.cursor = 0

    def drawSelf(self, canvas, draw_cursor=False):
        text_cursor = self.top_justification            #where to start text -> will move as items are written to canvas
        
        for item_i, item in enumerate(self.item_queue):          
            cursor_start = text_cursor
            lines = item.text.splitlines()
            
            text_cursor += 15
            cv2.putText(canvas, f"{item.quantity} {lines[0]}" , (self.left_justification, text_cursor), 5, .7, (255,255,255), 1, lineType=16)
            cv2.putText(canvas, f"{str(int((time.time()-item.time)//60))}" , (self.left_justification+240, text_cursor), 5, .7, (255,255,255), 1, lineType=16)
            
            for line in lines[1:]:
                text_cursor += 15
                cv2.putText(canvas, f" {line}", (self.left_justification, text_cursor), 5, .7, (255,255,255), 1, lineType=16)
            
            if item_i == self.cursor and draw_cursor:
                canvas[cursor_start+2:text_cursor+3, 0:canvas.shape[1]-1] = ~canvas[cursor_start+2:text_cursor+3, 0:canvas.shape[1]-1]