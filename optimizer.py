import time
import cv2

class ListItem:
    def __init__(self, text, quantity, modification = None):
        self.text = text
        self.quantity = quantity
        self.time_list = []
        #self.mod_list = []
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
    def __init__(self):
        self.time = time.time()

class OrderOptimizer:
    def __init__(self):
        self.order_queue = []
        self.item_queue = []
        self.item_set = set()

        self.cursor = 0

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
                        #queued_item.mod_list.append(item.modification)


    def remove(self, item):
        if item in self.item_set:
            for queued_item in self.item_queue:
                if queued_item == item:
                    if queued_item.quantity > item.quantity:
                        queued_item.quantity -= item.quantity

                        for n in range(item.quantity):
                            queued_item.time_list.pop(0)

                        queued_item.time = queued_item.time_list[0]

                    else:
                        self.item_queue.remove(queued_item)
                        self.item_set.remove(queued_item)
                    
            self.reSort()

    def reSort(self):
        self.item_queue.sort()
        self.incrementCursor(0)

    def attachCursor(self, _cursor):
        self.cursor = _cursor

    def incrementCursor(self, val):
        if len(self.item_queue):
            self.cursor = (self.cursor + val) % len(self.item_queue)
        else:
            self.cursor = 0

    def drawSelf(self, canvas):
        for item in range(len(self.item_queue)):
            cv2.putText(canvas, str(self.item_queue[item]), (10, 15 + 15*item), 5, .7, (255,255,255), 1, lineType=16)
            if item == self.cursor:
                cv2.rectangle(canvas, (0, 2 + item * 15), (324, 3 + (item+1) * 15), color = (255, 255, 255))
