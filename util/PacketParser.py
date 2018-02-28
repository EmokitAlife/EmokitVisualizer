class PacketParser:
    def fromCSVToPacket(self, headers, row):
        return ParsedPacket( headers, row )

    def fromPacketToCSV(self, packet):
        row_file = ""
        row_file += str(packet.timestamp) + ","
        row_file += str(packet.sensors['F3']['value']) + ","
        row_file += str(packet.sensors['F3']['quality']) + ","
        row_file += str(packet.sensors['FC5']['value']) + ","
        row_file += str(packet.sensors['FC5']['quality']) + ","
        row_file += str(packet.sensors['F7']['value']) + ","
        row_file += str(packet.sensors['F7']['quality']) + ","
        row_file += str(packet.sensors['T7']['value']) + ","
        row_file += str(packet.sensors['T7']['quality']) + ","
        row_file += str(packet.sensors['P7']['value']) + ","
        row_file += str(packet.sensors['P7']['quality']) + ","
        row_file += str(packet.sensors['O1']['value']) + ","
        row_file += str(packet.sensors['O1']['quality']) + ","
        row_file += str(packet.sensors['O2']['value']) + ","
        row_file += str(packet.sensors['O2']['quality']) + ","
        row_file += str(packet.sensors['P8']['value']) + ","
        row_file += str(packet.sensors['P8']['quality']) + ","
        row_file += str(packet.sensors['T8']['value']) + ","
        row_file += str(packet.sensors['T8']['quality']) + ","
        row_file += str(packet.sensors['F8']['value']) + ","
        row_file += str(packet.sensors['F8']['quality']) + ","
        row_file += str(packet.sensors['AF4']['value']) + ","
        row_file += str(packet.sensors['AF4']['quality']) + ","
        row_file += str(packet.sensors['FC6']['value']) + ","
        row_file += str(packet.sensors['FC6']['quality']) + ","
        row_file += str(packet.sensors['F4']['value']) + ","
        row_file += str(packet.sensors['F4']['quality']) + ","
        row_file += str(packet.sensors['AF3']['value']) + ","
        row_file += str(packet.sensors['AF3']['quality']) + ","
        row_file += str(packet.sensors['X']['value']) + ","
        row_file += str(packet.sensors['Y']['value']) + ","
        row_file += str(packet.sensors['Z']['value'])
        return row_file


class ParsedPacket:
    def __init__(self, headers, row):
        self.sensors = {}
        self.timestamp = row.pop(0)
        headers.pop(0)
        for header in headers:
            header = header.split()
            if header[0] not in self.sensors:
                self.sensors[header[0]] = {}
            value = row.pop(0)
            self.sensors[header[0]][header[1].lower()] = int(value) if value != "?" else None