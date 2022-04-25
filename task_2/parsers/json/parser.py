import os


class Parser:

    @staticmethod
    def lex():
        raise NotImplementedError()

    @staticmethod
    def parse(self):
        raise NotImplementedError()

    @staticmethod
    def serialize(self):
        raise NotImplementedError()

    @classmethod
    def dump(cls, obj, pf, is_pickle=False):
        my_str = cls.serialize(obj)
        try:
            if pf[:2] == './':
                pf = pf[2:]
            if os.path.isfile(pf):
                print('File by this path will be overridden')
            if is_pickle is False:
                file = open(pf, 'w')
            else:
                file = open(pf, 'wb')
            file.write(my_str)
            file.close()
        except FileNotFoundError as e:
            print('There is no such file by path: ' + pf)

    @classmethod
    def dumps(cls, obj):
        return cls.serialize(obj)

    @classmethod
    def load(cls, pf, is_pickle=False, is_buffer=False):
        if pf[:2] == './':
            pf = pf[2:]
        try:
            if is_pickle is False:
                file = open(pf, 'r')
            else:
                file = open(pf, 'rb')
            my_str = file.read()
            return cls.loads(my_str, is_buffer)
        except FileNotFoundError as e:
            print('There is no such file by path: ' + pf)

    @classmethod
    def loads(cls, my_str, is_buffer=False):
        json = cls.parse(my_str, is_buffer)
        return json
