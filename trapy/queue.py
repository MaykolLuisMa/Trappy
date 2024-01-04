class queue:
    def __init__(self):
        self.elements = []
        self.first = None
    
    def peek(self):
        return self.first
    
    def pop(self):
        if (len(self.elements) == 0):
            return None
        if (len(self.elements) == 1):
            self.first = None
        else: self.first = self.elements[1]
        self.elements.pop(0)
        
    def push(self, element):
        if (len(self.elements) == 0):
            self.first = element
        self.elements.append(element)

    def isEmpty(self):
        return (self.peek() == None)
