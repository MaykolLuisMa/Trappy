import time

class Chronometer:
    def __init__(self):
        self.time_to_wait = 0
        self.start_time = None
        self.finished = None
        
    def _refresh(self):
        if (self.finished == None):
            self.finished = True
        
        if (not self.finished and self.start_time != None):
            self.finished = time.time - self.start_time >= self.time_to_wait

        if (self.start_time != None and self.finished):
            self.start_time = None
            self.time_to_wait = 0
    
    def start(self, wait = 3):
        self._refresh()
        if(self.start_time != None):
            assert("This chronometer is already in use")
            return
        self.time_to_wait = wait
        self.start_time = time.time()
        self.finished = False
        
    def time_left(self):
        if (self.finished == None):
            return -1
        if (self.timeout()):
            return -1
        return self.time_to_wait - (time.time() - self.start_time)
    
    def timeout(self):
        if (self.finished == None): 
            return False
        self._refresh()
        return self.finished