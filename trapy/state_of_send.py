from chronometer import *
from conn import *
import utils
class State_of_Send:
    def __init__(conn : Conn, data):
        chunks = utils.fragment_data(data, conn.max_data_size)
        global_timer = Chronometer()
        timers = [Chronometer() for _ in range(len(chunks))]
        conn_sender = conn
        

