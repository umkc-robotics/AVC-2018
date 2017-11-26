import json

# config reader exception class
class ConfigReaderException(Exception):
    pass


class ConfigReader(object):
    @staticmethod
    def read_json(location):
        with open(location, "r") as json_file:
            return json.load(json_file, object_pairs_hook=decode_unicode_hook)

# hook function to turn bytes in dictionary into strings
def decode_unicode_hook(json_pairs):
    """
    Given json pairs, properly encode strings into utf-8 for general usage
    :param json_pairs: dictionary of json key-value pairs
    :return: new dictionary of json key-value pairs in utf-8
    """
    new_json_pairs = []
    for key, value in json_pairs:
        if isinstance(value, unicode):
            value = value.encode("utf-8")
        if isinstance(key, unicode):
            key = key.encode("utf-8")
        new_json_pairs.append((key, value))
    return dict(new_json_pairs)
