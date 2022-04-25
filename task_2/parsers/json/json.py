from parser import Parser
from const import *
import inspect
import types


class Json(Parser):
    @staticmethod
    def serialize_str_int(key, value):
        if type(value) is str:
            value = JSON_QUOTE + value + JSON_QUOTE
        else:
            value = str(value)
        if type(key) is str:
            key = JSON_QUOTE + key + JSON_QUOTE
        else:
            key = str(key)
        return key + ':' + value

    @staticmethod
    def serialize(obj):
        string = '{'
        for key, value in obj.items():
            if type(value) is str or type(value) is int or type(value) is float or type(value) is complex:
                string += Json.serialize_str_int(key, value)
            if type(value) is dict:
                key_string = str(key)
                if type(key) is str:
                    key_string = JSON_QUOTE + key_string + JSON_QUOTE
                string += key_string + ':' + Json.serialize(value)
            if type(value) is type:
                key_string = str(key)
                if type(key) is str:
                    key_string = JSON_QUOTE + key_string + JSON_QUOTE
                string += key_string + ':' + Json.serialize_class(value)
            if callable(value) and type(value) is not type:
                key_string = str(key)
                if type(key) is str:
                    key_string = JSON_QUOTE + key_string + JSON_QUOTE
                string += key_string + ':' + Json.serialize_function(value)
            if type(value) is list:
                key_string = str(key)
                if type(key) is str:
                    key_string = JSON_QUOTE + key_string + JSON_QUOTE
                string += key_string + ':' + Json.serialize_list(value)
            string += JSON_COMMA
        string = string[:(len(string) - 1)] + '}'
        return string

    @staticmethod
    def serialize_list(val):
        string = '['
        for value in val:
            string += JSON_QUOTE + str(value) + JSON_QUOTE + ', '
        string = string[:(len(string) - 2)] + ']'
        return string

    @staticmethod
    def serialize_function(func):
        true_func_name = func.__name__
        if type(func) is types.LambdaType and func.__name__ == '<lambda>':
            func_name = inspect.getsource(func).split('=')[0]
            func_name = func_name.strip()
            true_func_name = func_name
        func_source = inspect.getsource(func)
        f_glob = {}
        var_arr = []
        if func_source.__contains__('global'):
            var_arr = func_source.split('global')
            for ind in range(len(var_arr)):
                var_arr[ind] = var_arr[ind][:var_arr[ind].find('\n')].lstrip()
            var_arr.pop(0)
        for ind in range(len(var_arr)):
            f_glob[var_arr[ind]] = func.__globals__[var_arr[ind]]
        f_str = ''
        if var_arr:
            f_str = ', "globals": ' + Json.serialize(f_glob)
        func_name = '{"func_name": "' + true_func_name + JSON_QUOTE + f_str
        return func_name + ', "code":' + JSON_QUOTE + func_source + JSON_QUOTE + '}'

    @staticmethod
    def serialize_class(cls):  # TODO: sort built-in and custom attributes the right way
        functions = inspect.getmembers(cls, predicate=inspect.isfunction)
        supers = ''
        if cls.__bases__[0] != "object":
            for cl in cls.__bases__:
                if cl.__name__ != 'object':
                    supers += ',"supers":' + Json.serialize_class(cl)
        else:
            supers = ',"supers":' + '"None"'
        if len(functions) > 0:
            func_string = '"funcs":{'
            for func in functions:
                func_source = inspect.getsource(func[1])
                func_body_lines = func_source.split('\n')
                for ind in range(len(func_body_lines) - 1):
                    func_body_lines[ind] = func_body_lines[ind][4:]
                func_source = "\n".join(func_body_lines)
                func_string += '"' + func[0] + '":{"func_name":"' + func[0] + '","code":"' + func_source + '"},'
            func_string = func_string[:(len(func_string) - 1)] + '},'
        else:
            func_string = '"funcs":"None",'
        string = '{"classname":' + JSON_QUOTE + cls.__name__ + JSON_QUOTE + JSON_COMMA
        attr = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))
        real_attr = [a for a in attr if not (a[0].startswith('__') and a[0].endswith('__'))]
        if len(real_attr) > 0:
            attr_string = '"attrs":{'
            for at in real_attr:
                attr_string += JSON_QUOTE + at[0] + JSON_QUOTE + \
                               ':' + \
                               JSON_QUOTE + at[1] + JSON_QUOTE + \
                               JSON_COMMA
            attr_string = attr_string[:(len(attr_string) - 1)] + '}'
        else:
            attr_string = '"attrs":"None"'
        string = string + func_string + attr_string + supers + '}'
        return string

    @staticmethod
    def lex_string(string):
        json_string = ''

        if string[0] == JSON_QUOTE:
            string = string[1:]
        else:
            return None, string

        for c in string:
            if c == JSON_QUOTE:
                return json_string, string[len(json_string) + 1:]
            else:
                json_string += c

        raise Exception('Expected end-of-string quote')

    @staticmethod
    def lex_number(string):
        json_number = ''

        number_characters = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '-', 'e', '.']

        for c in string:
            if c in number_characters:
                json_number += c
            else:
                break

        rest = string[len(json_number):]

        if not len(json_number):
            return None, string

        if '.' in json_number:
            return float(json_number), rest

        return int(json_number), rest

    @staticmethod
    def lex_bool(string):
        string_len = len(string)

        if string_len >= TRUE_LEN and \
                string[:TRUE_LEN] == 'true':
            return True, string[TRUE_LEN:]
        elif string_len >= FALSE_LEN and \
                string[:FALSE_LEN] == 'false':
            return False, string[FALSE_LEN:]

        return None, string

    @staticmethod
    def lex_null(string):
        string_len = len(string)

        if string_len >= NULL_LEN and \
                string[:NULL_LEN] == 'null':
            return True, string[NULL_LEN:]

        return None, string

    @staticmethod
    def lex(string):
        tokens = []

        while len(string):
            json_string, string = Json.lex_string(string)
            if json_string is not None:
                tokens.append(json_string)
                continue

            json_number, string = Json.lex_number(string)
            if json_number is not None:
                tokens.append(json_number)
                continue

            json_bool, string = Json.lex_bool(string)
            if json_bool is not None:
                tokens.append(json_bool)
                continue

            json_null, string = Json.lex_null(string)
            if json_null is not None:
                tokens.append(None)
                continue

            if string[0] in JSON_WHITESPACE:
                string = string[1:]
            elif string[0] in JSON_SYNTAX:
                tokens.append(string[0])
                string = string[1:]
            else:
                raise Exception('Unexpected character: {}'.format(string[0]))

        return tokens

    @staticmethod
    def parse_array(tokens, is_buffer):
        json_array = []

        t = tokens[0]
        if t == JSON_RIGHTBRACKET:
            return json_array, tokens[1:]

        while True:
            json, tokens = json.parse_json(tokens, is_buffer)
            json_array.append(json)

            t = tokens[0]
            if t == JSON_RIGHTBRACKET:
                return json_array, tokens[1:]
            elif t != JSON_COMMA:
                raise Exception('Expected comma after object in array')
            else:
                tokens = tokens[1:]

        raise Exception('Expected end-of-array bracket')

    @staticmethod
    def parse_object(tokens, is_buffer=False):
        json_object = {}

        t = tokens[0]
        if t == JSON_RIGHTBRACE:
            return json_object, tokens[1:]

        while True:
            json_key = tokens[0]
            if type(json_key) is str or type(json_key) is int:
                tokens = tokens[1:]
            else:
                raise Exception('Expected string key, got: {}'.format(json_key))

            if tokens[0] != JSON_COLON:
                raise Exception('Expected colon after key in object, got: {}'.format(t))

            json_value, tokens = Json.parse_json(tokens[1:], is_buffer)

            if type(json_value) is not int and "code" in json_value and is_buffer is False:
                func_object = {}
                if "globals" in json_value:
                    func_object = json_value["globals"]
                exec(json_value["code"], func_object)
                json_object[json_key] = func_object[json_value["func_name"]]
            elif type(json_value) is not int and "classname" in json_value and is_buffer is False:
                attr_dict = {}
                super_tuple = tuple()
                if json_value["attrs"] != 'None' and json_value["attrs"] != {}:
                    for attr in json_value["attrs"]:
                        attr_dict[attr] = json_value["attrs"][attr]
                if json_value["funcs"] != 'None' and json_value["funcs"] != {}:
                    for func in json_value["funcs"]:
                        attr_dict[func] = json_value["funcs"][func]
                if "supers" in json_value and json_value["supers"] != 'None' and json_value["supers"] != {}:
                    super_tuple += (json_value["supers"],)
                json_object[json_key] = type(
                    json_value["classname"],
                    super_tuple,
                    attr_dict
                )
            else:
                json_object[json_key] = json_value

            t = tokens[0]
            if t == JSON_RIGHTBRACE:
                return json_object, tokens[1:]
            elif t != JSON_COMMA:
                raise Exception('Expected comma after pair in object, got: {}'.format(t))

            tokens = tokens[1:]

        raise Exception('Expected end-of-object bracket')

    @staticmethod
    def parse(my_str, is_buffer=False):
        tokens = Json.lex(my_str)
        json, tokens = Json.parse_json(tokens, is_buffer)
        return json

    @staticmethod
    def parse_json(tokens, is_buffer, is_root=False):
        t = tokens[0]

        if is_root and t != JSON_LEFTBRACE:
            raise Exception('Root must be an object')

        if t == JSON_LEFTBRACKET:
            return Json.parse_array(tokens[1:], is_buffer)
        elif t == JSON_LEFTBRACE:
            return Json.parse_object(tokens[1:], is_buffer)
        else:
            return t, tokens[1:]
