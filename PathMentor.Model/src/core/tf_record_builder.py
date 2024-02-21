import tensorflow as tf

class TFRecordBuilder:
    def __init__(self, path):
        self.path = path
        self.writer = tf.io.TFRecordWriter(self.path)

    @staticmethod
    def _bytes_feature(value):
        """Returns a bytes_list from a string / byte."""
        if isinstance(value, type(tf.constant(0))):
            value = value.numpy()
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

    @staticmethod
    def _bytes_feature_list(values):
        """Returns a bytes_list from a list of string / byte."""
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=values))

    def serialize_example(self, **kwargs):
        """Serializes an example into TFRecord format."""
        feature = {key: self._serialize_value(value) for key, value in kwargs.items()}
        example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
        return example_proto.SerializeToString()

    def _serialize_value(self, value):
        """Determines how to serialize the values."""
        if isinstance(value, list):
            if all(isinstance(v, bytes) for v in value):
                return self._bytes_feature_list(value)
        elif isinstance(value, bytes):
            return self._bytes_feature(value)
        else:
            raise ValueError("Unsupported feature type")

    def write_example(self, example):
        """Writes a serialized example to the TFRecord."""
        self.writer.write(example)

    def close(self):
        """Closes the TFRecord writer."""
        self.writer.close()
