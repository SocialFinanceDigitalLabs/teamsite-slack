import json
from base64 import b85decode, b85encode


def encode_action(**kwargs):
    """
    Encodes the keyword arguments

    >>> encode_action(hello="world", goodbye="java")
    'dm?CMY;12LIv^r<Z*pv8A}k;xXK!z0VtHjEIv^ryVRm66eE'

    :param kwargs:
    :return:
    """
    value = json.dumps(kwargs)
    return b85encode(value.encode("utf-8")).decode("utf-8")


def decode_action(value):
    """
    Decodes an encoded action

    >>> decode_action('dm?CMY;12LIv^r<Z*pv8A}k;xXK!z0VtHjEIv^ryVRm66eE')
    {'hello': 'world', 'goodbye': 'java'}

    :param value:
    :return:
    """
    value = b85decode(value.encode("utf-8")).decode("utf-8")
    return json.loads(value)
