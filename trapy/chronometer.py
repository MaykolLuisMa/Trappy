import time

class Chronometer:
    def __init__(self):
        self._time_to_wait = 0
        self._start_time = None
        self._finished = None
        
    def _refresh(self):
        if (self._finished == None):
            self._finished = True
        
        if (not self._finished and self._start_time != None):
            self._finished = time.time - self._start_time >= self._time_to_wait

        if (self._start_time != None and self._finished):
            self._start_time = None
            self._time_to_wait = 0
    
    def start(self, wait = 3):
        self._refresh()
        if(self._start_time != None):
            assert("This chronometer is already in use")
            return
        self._time_to_wait = wait
        self._start_time = time.time()
        self._finished = False
        
    def time_left(self):
        if (self._finished == None):
            return 0
        if (self.timeout()):
            return 0
        return self._time_to_wait - (time.time() - self._start_time)
    
    def timeout(self):
        if (self._finished == None): 
            return False
        self._refresh()
        return self._finished