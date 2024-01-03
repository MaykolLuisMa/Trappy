from conn import Conn
from trapy import *
import sys
B = listen("127.0.0.1:7200")
accept(B)
data_raw = recv(B, 512)
print(sys.getsizeof(data_raw))
print(data_raw)