import collections
class queue:
    def __init__(self):
        self.elements = collections.deque()
    
    def peek(self, pos = 0):
        return self.elements[pos]
    
    def pop(self):
        return self.elements.popleft()
        
    def push(self, element):
        self.elements.append(element)

    def empty(self):
        return (self.size() == 0)
    
    def size(self):
        return len(self.elements)