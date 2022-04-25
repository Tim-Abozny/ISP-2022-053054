from parser import Parser
import pickle


class Pickle(Parser):
    @staticmethod
    def serialize(obj):
        my_str = pickle.dumps(obj)
        return my_str

    @staticmethod
    def parse(my_str, is_buffer=False):
        obj = pickle.loads(my_str)
        return obj
