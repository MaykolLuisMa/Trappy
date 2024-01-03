from conn import Conn
from trapy import *

B = listen("127.0.0.1:7200")
accept(B)
data_raw = recv(B, 300)
print(data_raw)