import cv2

class Element:
    def __init__(self, ID, x_pos = 0, y_pos = 0, width = 0, height = 0, color = (0, 0, 0), border_color = (0, 0, 0), text_color = (0, 0, 0), texture = None):
        self.ID = ID

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_pos2 = x_pos + width
        self.y_pos2 = y_pos + height
        self.width = width
        self.height = height

        self.color = color
        self.border_color = border_color
        self.text_color = text_color

        self.font_size = .7

        self.texture = texture

class Button(Element):
    def __init__(self, text, ID, x_pos = 0, y_pos = 0, width = 0, height = 0, color = (0, 0, 0), border_color = (0, 0, 0), text_color = (0, 0, 0), texture = None):
        super().__init__(ID, x_pos, y_pos, width, height, color, border_color, text_color, texture)
        self.text = text
        self.callback = None

    def addCallback(self, _call_back_function):
        self.callback = _call_back_function

class Counter(Element):
    def __init__(self, val, ID, x_pos = 0, y_pos = 0, width = 0, height = 0, color = (0, 0, 0), border_color = (0, 0, 0), text_color = (0, 0, 0)):
        super().__init__(ID, x_pos, y_pos, width, height, color, border_color, text_color)
        self.val = val
        self.text = str(val)

    def increment(self, val):
        self.val += val
        self.text = str(self.val)


class Panel:
    def __init__(self, text, x_pos, y_pos, width, height, color, transparent = False):
        self.text = text

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_pos2 = x_pos + width
        self.y_pos2 = y_pos + height
        self.width = width
        self.height = height

        self.transparent = transparent
        self.color = color

        self.elements = set()

    def addElement(self, element):
        self.elements.add(element)

        self.setAbsoluteElementPos(element, self.x_pos + element.x_pos, self.y_pos + element.y_pos, element.width, element.height)

    def setAbsoluteElementPos(self, element, x, y, width, height):
        element.x_pos = x
        element.y_pos = y
        element.x_pos2 = x + width
        element.y_pos2 = y + height
        element.width = width
        element.height = height
    
    def drawSelf(self, canvas):
        if not self.transparent:
            cv2.rectangle(canvas, (self.x_pos, self.y_pos), (self.x_pos + self.width, self.y_pos + self.height), self.color, -1)

        for element in self.elements:
            if element.texture is None:
                cv2.rectangle(canvas, (element.x_pos, element.y_pos), (element.x_pos2, element.y_pos2), element.color, -1)
                cv2.rectangle(canvas, (element.x_pos, element.y_pos), (element.x_pos2, element.y_pos2), element.border_color, 1)
                cv2.putText(canvas, element.text, (element.x_pos + 6, element.y_pos + element.height // 2 + 6), 4, .7, element.text_color, 1, lineType=16)
            else:
                canvas[element.y_pos : element.y_pos + element.height, element.x_pos : element.x_pos + element.width,:] = element.texture[0 : element.height, 0 : element.width,:]
                cv2.rectangle(canvas, (element.x_pos, element.y_pos), (element.x_pos2, element.y_pos2), element.border_color, 1)
                

class GridPanel(Panel):
    def __init__(self, rows, columns, padding, text, x_pos, y_pos, width, height, color, transparent = False):
        super().__init__(text, x_pos, y_pos, width, height, color)
        self.rows = rows
        self.columns = columns

        self.padding = padding

        self.element_width = (width - padding*(columns + 1)) // columns
        self.element_height = (height - padding*(rows + 1)) // rows

        self.element_grid = list(range(rows*columns))

    def addElement(self, element, row, col):
        self.element_grid[row*self.columns + col] = element
        self.elements.add(element)

        self.setAbsoluteElementPos(element, self.x_pos + self.padding*(1 + col) + self.element_width*(col), self.y_pos + self.padding*(1 + row) + self.element_height*(row), self.element_width, self.element_height)

    def drawSelf(self, canvas):
        if not self.transparent:
            cv2.rectangle(canvas, (self.x_pos, self.y_pos), (self.x_pos + self.width, self.y_pos + self.height), self.color, -1)

        for row in range(self.rows):
            for col in range(self.columns):
                if isinstance(self.element_grid[row*self.columns + col], Element):
                    if self.element_grid[row*self.columns + col].texture is None:
                        cv2.rectangle(canvas, (self.x_pos + self.padding*(1 + col) + self.element_width*(col), self.y_pos + self.padding*(1 + row) + self.element_height*(row)), (self.x_pos + self.padding*(1 + col) + self.element_width*(col+1), self.y_pos + self.padding*(1 + row) + self.element_height*(row+1)), self.element_grid[row*self.columns + col].color, -1)
                        cv2.rectangle(canvas, (self.x_pos + self.padding*(1 + col) + self.element_width*(col), self.y_pos + self.padding*(1 + row) + self.element_height*(row)), (self.x_pos + self.padding*(1 + col) + self.element_width*(col+1), self.y_pos + self.padding*(1 + row) + self.element_height*(row+1)), (156, 112, 168), 1)
                        cv2.putText(canvas, self.element_grid[row*self.columns + col].text, (self.x_pos + self.padding*(1 + col) + self.element_width*(col) + 6, self.y_pos + self.padding*(1 + row) + self.element_height*(row) + self.element_height // 2 + 6), 4, self.element_grid[row*self.columns + col].font_size, self.element_grid[row*self.columns + col].text_color, 1, lineType=16)
                    else:
                        canvas[element.y_pos : element.y_pos + element.height, element.x_pos : element.x_pos + element.width,:] = element.texture[0 : element.height, 0 : element.width,:]
                        cv2.rectangle(canvas, (self.x_pos + self.padding*(1 + col) + self.element_width*(col), self.y_pos + self.padding*(1 + row) + self.element_height*(row)), (self.x_pos + self.padding*(1 + col) + self.element_width*(col+1), self.y_pos + self.padding*(1 + row) + self.element_height*(row+1)), (156, 112, 168), 1)

