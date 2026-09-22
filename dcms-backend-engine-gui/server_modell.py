class Server:
    def __init__(self, name, ip, os):
        self.name = name
        self.status = "offline"
        self.ip = ip
        self.os = os

    def ping(self):
        return self.status == "online"

    def status_wechseln(self):
        if self.status == "offline":
            self.status = "online"
        else:
            self.status = "offline"

class Webserver(Server):
    def __init__(self, name, ip, os, domain, ssl_aktiv):
        super().__init__(name, ip, os)
        self.domain = domain
        self.ssl_aktiv = ssl_aktiv

class DatenbankServer(Server):
    def __init__(self, name, ip, os, db_typ, port):
        super().__init__(name, ip, os)
        self.db_typ = db_typ
        self.port = port
