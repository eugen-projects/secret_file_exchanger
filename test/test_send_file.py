import socket
import threading
import unittest

from exchanger.main import *


class PacketReceiverMock(object):
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
        self.sock.listen(1)
        threading.Thread(target=self.accept_connection)
        self.messages = []
        self._terminate = threading.Event()
        self.connection = None

    def accept_connection(self):
        self.connection, _ = self.sock.accept()
        self.connection.settimeout(0.5)
        while not self._terminate.isSet():
            try:
                msg = self.connection.recv(4096)
                if msg:
                    self.messages.append(msg)
            except socket.timeout:
                pass

    def close(self):
        self._terminate.set()
        if self.connection:
            self.connection.close()
        self.sock.close()

    def get_messages(self):
        return list(self.messages)


class TestUploaderUtilities(unittest.TestCase):
    def setUp(self):
        self.uploader = UploadSession()

    def test_invalid_files(self):
        self.assertRaises(TerminateProgram, self.uploader._get_file_sizes, ["somwhere/bla bla.txt"])

    def test_valid_file_size(self):
        result = self.uploader._get_file_sizes(['test/test_send_file.py'])
        for k, v in result.iteritems():
            self.assertGreaterEqual(v, 0)


class TestUploader(unittest.TestCase):
    IP = 'localhost'
    PORT = 3065

    def setUp(self):
        self.uploader = UploadSession()
        self.receiver = PacketReceiverMock(TestUploader.IP, TestUploader.PORT)

    def tearDown(self):
        self.receiver.close()

    def test_connection(self):
        self.uploader.connect(self.IP, self.PORT, ['test_send_file.py'])