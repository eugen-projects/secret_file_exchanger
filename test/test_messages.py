import copy
import cPickle
import struct
import unittest

from exchanger.messages import Message


class TestMessage(Message):
    def __init__(self, bytes, count):
        super(TestMessage, self).__init__()
        self.c = count
        self.b = bytes


class MessageTests(unittest.TestCase):
    def test_message_serialization(self):
        bytestream = TestMessage('Eugen', 5).serialize()

        message = cPickle.dumps({'b': 'Eugen', 'c': 5}, cPickle.HIGHEST_PROTOCOL)
        payload = struct.pack("!i%ds" % len(message), len(message), message)

        self.assertLess(len(bytestream), 4+len(cPickle.dumps(TestMessage('Eugen', 5))))
        self.assertEquals(payload, bytestream,
                          '\nExpected: %s\nActual:   %s' % (repr(payload), repr(bytestream)))

    def test_message_deserialization(self):
        obj = TestMessage('Andi', 4)

        message = cPickle.dumps({'b': 'Eugen', 'c': 5, 'e': 'new-field'}, cPickle.HIGHEST_PROTOCOL)
        payload = struct.pack("!i%ds" % len(message), len(message), message)

        obj.deserialize(payload)
        self.assertEquals('Eugen', obj.b)
        self.assertEquals(5, obj.c)
        self.assertEquals('new-field', obj.e)

    def test_message_restore(self):
        obj = TestMessage('abcs', 4)
        obj_copy = copy.deepcopy(obj)
        obj.deserialize(obj.serialize())
        self.assertEqual(obj_copy, obj, "\nExpected: %s\nActual:   %s" % (obj_copy.__dict__, obj.__dict__))