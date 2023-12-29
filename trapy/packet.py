from struct import pack, unpack

class Packet:
    def __init__(self):
        self.tcp_source_port = None
        self.tcp_dest_port = None
        self.tcp_seq = None
        self.tcp_ack_seq = None
        self.tcp_offset_res = None
        
        # self.tcp_flag_syn = 0
        # self.tcp_flag_ack = 0
        # self.tcp_flag_rst = 0
        # self.tcp_flag_psh = 0
        # self.tcp_flag_urg = 0
        # self.tcp_flag_fin = 0
        
        # self._tcp_flags = 0
        
        self.tcp_flags = 0
        
        self.tcp_window = None
        self.tcp_check = None
        self.tcp_urg_ptr = None
        
        self.ip_source_host = None
        self.ip_dest_host = None
        
        self._ip_header = None
        
        self.data = None
    
    def get(self, packet_from_raw):
        self.ip_header = unpack("!BBHHHBBH4s4s", packet_from_raw[0:20]) 
           
        self.source_host = self.ip_header[8]
        self.dest_host = self.ip_header[9]
        
        self.tcp_source_port, self.tcp_dest_port, self.tcp_seq, self.tcp_ack_seq, self.tcp_offset_res, self.tcp_flags, self.tcp_window, self.tcp_check, self.tcp_urg_ptr, = unpack("!HHLLBBHHH", packet_from_raw[20:40])
        
        self.data = packet_from_raw[40:]
    
    def _refresh(self):
        self._ip_header[8] = self.ip_source_host
        self._ip_header[9] = self.ip_dest_host
        
        # self._tcp_flags = (
        #     self.tcp_fin
        #     + (self.tcp_syn << 1)
        #     + (self.tcp_rst << 2)
        #     + (self.tcp_psh << 3)
        #     + (self.tcp_ack << 4)
        #     + (self.tcp_urg << 5)
        # )
    
    def build(self):
        self._refresh()
        tcp_header = pack(
            "!HHLLBBHHH",
            self.tcp_source_port,
            self.tcp_dest_port,
            self.tcp_seq,
            self.tcp_ack_seq,
            self.tcp_offset_res,
            self.tcp_flags,
            self.tcp_window,
            self.tcp_check,
            self.tcp_urg_ptr,
        )
        ip_header = pack(
            "!BBHHHBBH4s4s", 
            self._ip_header[0],
            self._ip_header[1],
            self._ip_header[2],
            self._ip_header[3],
            self._ip_header[4],
            self._ip_header[5],
            self._ip_header[6],
            self._ip_header[7],
            self._ip_header[8],
            self._ip_header[9],
        )
        
        return ip_header + tcp_header + self.data


