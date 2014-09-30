import socket
import threading
import unittest

from exchanger.main import *


class TestUploaderUtilities(unittest.TestCase):
    def setUp(self):
        self.uploader = UploadSession()

    def test_invalid_files(self):
        self.assertRaises(TerminateProgram, self.uploader._get_file_sizes, ["somwhere/bla bla.txt"])

    def test_valid_file_size(self):
        result = self.uploader._get_file_sizes(['test/test_send_file.py'])
        for k, v in result.iteritems():
            self.assertGreaterEqual(v, 0)