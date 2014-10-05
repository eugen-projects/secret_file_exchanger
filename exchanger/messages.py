import cPickle
import struct


class Message(object):

    def pre_serialize(self, message):
        return message

    def post_deserialize(self, message):
        return message

    def serialize(self, protocol=cPickle.HIGHEST_PROTOCOL):
        message = cPickle.dumps(self.__dict__, protocol)
        message = self.pre_serialize(message)
        len_message = len(message)
        payload = struct.pack('!i%ds' % len_message, len_message, message)
        return payload

    def deserialize(self, payload):
        message_length = struct.unpack_from('!i', payload, 0)[0]
        message = struct.unpack_from('!%ds' % message_length, payload, 4)[0]
        message = self.post_deserialize(message)
        state = cPickle.loads(message)
        self.__dict__.update(state)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

