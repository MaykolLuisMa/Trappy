from struct import pack, unpack

class Packet:
    def __init__(self):
        self.tcp_source = None
        self.tcp_dest = None
        self.tcp_seq = None
        self.tcp_ack_seq = None
        self.tcp_offset_res = None
        
        self.tcp_flag_syn = None
        self.tcp_flag_ack = None
        self.tcp_flag_rst = None
        self.tcp_flag_psh = None
        self.tcp_flag_urg = None
        self.tcp_flag_fin = None
        
        self._tcp_flags = None
        
        self.tcp_window = None
        self.tcp_check = None
        self.tcp_urg_ptr = None
        
        self.source_host = None
        self.dest_host = None
        
        self._ip_header = None
        
        self.data = None
    
    def get(self, packet_from_raw):
        self.ip_header = unpack("!BBHHHBBH4s4s", packet_from_raw[0:20]) 
           
        self.source_host = self.ip_header[8]
        self.dest_host = self.ip_header[9]
        
        self.tcp_source, self.tcp_dest, self.tcp_seq, self.tcp_ack_seq, self.tcp_offset_res, self.tcp_flags, self.tcp_window, self.tcp_check, self.tcp_urg_ptr, = unpack("!HHLLBBHHH", packet_from_raw[20:40])
        
        self.data = packet_from_raw[40:]
    
    def _refresh(self):
        self.ip_header[8] = self.source_host
        self.ip_header[9] = self.dest_host
        
        self._tcp_flags = (
            self.tcp_fin
            + (self.tcp_syn << 1)
            + (self.tcp_rst << 2)
            + (self.tcp_psh << 3)
            + (self.tcp_ack << 4)
            + (self.tcp_urg << 5)
        )
    
    def build(self):
        self._refresh()
        tcp_header = pack(
            "!HHLLBBHHH",
            self.tcp_source,
            self.tcp_dest,
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
            self.ip_header[0],
            self.ip_header[1],
            self.ip_header[2],
            self.ip_header[3],
            self.ip_header[4],
            self.ip_header[5],
            self.ip_header[6],
            self.ip_header[7],
            self.ip_header[8],
            self.ip_header[9],
        )
        
        return ip_header + tcp_header + self.data


