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
        
def test_queue():
    q = queue()
    if (q.first != None):
        print("error")
        return
    for i in range(7):
        q.push(i)
    for i in range(7):
        if q.peek() != i: 
            print("error")
            return
        q.pop()
    if (q.first != None):
        print("error")
        return
    if (q.pop() != None):
        print("error")
        return
    print("accepted")

test_queue()