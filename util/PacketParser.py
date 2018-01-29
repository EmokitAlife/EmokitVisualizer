class PacketParser:
    def fromCSVToPacket(self, headers, row):
        packet = {}
        packet[ headers.pop(0).lower() ] = row.pop(0)
        packet.sensors = {}
        for header in headers:
            header = header.split()
            if header[0] not in packet:
                packet.sensors[header[0]] = {}
            packet.sensort[header[0]][header[1].lower()] = row.pop(0)
        return packet
