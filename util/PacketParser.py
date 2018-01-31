class PacketParser:
    def fromCSVToPacket(self, headers, row):
        return ParsedPacket( headers, row )


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