from conn import *
from trapy import *
B = Conn()
B.bind()
dial(str(B.source_host) + " : " + str(B.source_port))
accept(B)