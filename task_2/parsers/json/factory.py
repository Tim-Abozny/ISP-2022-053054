from abc import ABC
from json import Json
from pickle import Pickle
from yaml import Yaml
from toml import Toml


class Creator(ABC):
    @staticmethod
    def create_serializer(obj={}, my_type='JSON', file_path=''):
        if my_type.lower() == 'json':
            parser = Json()
        elif my_type.lower() == 'pickle':
            parser = Pickle()
        elif my_type.lower() == 'yaml':
            parser = Yaml()
        elif my_type.lower() == 'toml':
            parser = Toml()
        else:
            raise Exception('Unknown type! Type must be JSON/Toml/Yaml/Pickle')

        if file_path == '':
            my_str = parser.dumps(obj)
            return my_str
        else:
            if my_type.lower() == 'pickle':
                parser.dump(obj, file_path, is_pickle=True)
            else:
                parser.dump(obj, file_path)
            return 'Done by path ' + file_path

    @staticmethod
    def create_deserializer(str='', my_type='JSON', file_path='', is_buffer=False):
        parser = None
        if my_type.lower() == 'json':
            parser = Json()
        elif my_type.lower() == 'pickle':
            parser = Pickle()
        elif my_type.lower() == 'toml':
            parser = Toml()
        elif my_type.lower() == 'yaml':
            parser = Yaml()
        else:
            raise Exception('Unknown type! Type must be JSON/Toml/Yaml/Pickle')

        if file_path == '':
            obj = parser.loads(str)
            return obj
        else:
            if my_type.lower() == 'pickle':
                obj = parser.load(file_path, is_pickle=True, isBuffer=is_buffer)
            else:
                obj = parser.load(file_path, isBuffer=is_buffer)
            return obj
