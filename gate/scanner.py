import serial
import datetime
import uuid
import threading as th

class Scanner(th.Thread):

    def __init__(self, device, reports_path):
        super().__init__()

        self.TAG_LENGTH = 8
        self.controller_name = device['name']
        self.addr = device['path']
        self.REPORTS_PATH = reports_path
        self.device = device
        self.connector = self._init_connector()
        self.work = False

    def _init_connector(self):
        ser = serial.Serial(self.addr)
        ser.baudrate = 57600
        ser.bytesize = serial.EIGHTBITS
        ser.parity = 'N'
        ser.stopbits = 1
        ser.startbits = 1
        ser.timeout = None
        ser.xonxoff = False
        ser.rtscts = False
        ser.dsrdtr = False
        print('Connector is created')
        print(f'Connection params: {ser}')
        return ser

    def _openPort(self):
        try:
            self.connector.close()
        except:
            pass
        self.connector.open()
        print(f'++++++++++ Port is opened ++++++++++')

    def closePort(self):
        self.connector.close()
        print(f'---------- Port is closed ----------')

    def run(self):
        self._init_connector()
        self._openPort()
        print(f'Devise {self.controller_name} has started')
        self.work = True
        old_tag = None
        
        
        while self.work:
            tag = ""
            raw_data = self.connector.read(self.TAG_LENGTH + 6)
            print ("-".join(hex(x) for x in raw_data))
            if (len(raw_data) < self.TAG_LENGTH + 6):
                continue
            tag = raw_data[4:12]
            if tag != old_tag and len(tag) != 0:
                old_tag = tag
                filename = self.REPORTS_PATH + "\\" + self.controller_name + '_' + str(uuid.uuid4()) + '.txt'
                print(filename)
                with open(filename, "w", encoding='utf-8') as self.file:
                    tagstr= "-".join(hex(x) for x in tag)
                    record = f'{datetime.datetime.now()} ---> tag: {tagstr}'
                    print(f'record= {record}')
                    print(record, file=self.file, end='\n')
                raw_data = None

    def stop(self):
        self.work = False
        self.closePort()
        self.file.close()

