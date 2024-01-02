from conn import Conn
from trapy import *

B = Conn()
B.bind("127.0.0.1", 7200)
accept(B)