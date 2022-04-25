import unittest
from json import Json


class TestJSON(unittest.TestCase):
    def setUp(self):
        self.json = Json()

    def testSerialize_str_int(self):
        self.assertEqual(self.json.serialize_str_int(1, "a"), '1:"a"')
        self.assertEqual(self.json.serialize_str_int("a", "a"), '"a":"a"')
        self.assertEqual(self.json.serialize_str_int("a", 1), '"a":1')
        self.assertEqual(self.json.serialize_str_int(1, 1), '1:1')

    def testSerialize_class(self):
        class B:
            pass

        class A(B):
            name = "name"

            def wow(self):
                print('who is who???')

        self.assertEqual(self.json.serialize_class(B), '{"classname":"B","funcs":"None","attrs":"None"}')
        self.assertEqual(self.json.serialize_class(A),
                         '{"classname":"A","funcs":{"wow":{"func_name":"wow","code":"        def wow(self):\n'
                         '            print(\'who is who???\')\n"}},"attrs":{"name":"name"},'
                         '"supers":{"classname":"B","funcs":"None","attrs":"None"}}')

    def testSerialize_functions(self):

        def test_func(testArg1, testArg2):
            print('this is test function')
            print(testArg2)
            return testArg1

        self.assertEqual(self.json.serialize_function(test_func),
                         '{"func_name": "testFunc", "code":"        def testFunc(testArg1, testArg2):\n '
                         '           print(\'this is test function\')\n            print(testArg2)\n'
                         '            return testArg1\n"}')

        def test_func2(args):
            a = 1 + 1 ** 10
            print(a)
            print('Some more unit tests')
            wow_units_tests_are_so_cool = 1 - 50000
            return wow_units_tests_are_so_cool

        self.assertEqual(self.json.serialize_function(test_func2),
                         '{"func_name": "testFunc2", "code":"        '
                         'def testFunc2(args):\n            a = 1 + 1 ** 10\n '
                         '           print(a)\n            print(\'Some more unit tests\')\n '
                         '           wow_units_tests_are_so_cool = 1 - 50000\n '
                         '           return wow_units_tests_are_so_cool\n"}')

    def testSerialize(self):
        self.assertEqual(self.json.serialize({2: "b"}), '{2:"b"}')
        self.assertEqual(self.json.serialize({"b": "b"}), '{"b":"b"}')
        self.assertEqual(self.json.serialize({"b": 2}), '{"b":2}')
        self.assertEqual(self.json.serialize({2: 2}), '{2:2}')
        self.assertEqual(self.json.serialize({"level1": {"level2": {"level3": 42}}, 13: 37}),
                         '{"level1":{"level2":{"level3":42}},13:37}')

        class C:
            pass

        class B(C):
            pass

        class A(B):
            name = 'name'
            age = 'test'

            def __init__(self):
                print('init')

            def test(self):
                print('test1')
                print('test12')

            def test2(self):
                print('test21')
                print('test22')

        def testing():
            print('31')
            print('32')
            return 5

        self.assertEqual(self.json.serialize({"b": A, "c": testing, "a": 1}),
                         '{"b":{"classname":"A","funcs":{"__init__":{"func_name":"__init__","code":" '
                         '       def __init__(self):\n            '
                         'print(\'init\')\n"},"test":{"func_name":"test","code":" '
                         '       def test(self):\n            print(\'test1\')\n '
                         '           print(\'test12\')\n"},"test2":{"func_name":"test2","code":" '
                         '       def test2(self):\n            print(\'test21\')\n      '
                         '      print(\'test22\')\n"}},"attrs":{"age":"test","name":"name"},"supers":'
                         '{"classname":"B","funcs":"None","attrs":"None","supers":{"classname":'
                         '"C","funcs":"None","attrs":"None"}}},"c":{"func_name": "testing", "code":" '
                         '       def testing():\n            print(\'31\')\n            '
                         'print(\'32\')\n            return 5\n"},"a":1}')

    def testSerialize_lambda(self):
        fff = lambda: 6
        obj = {"a": lambda: 6}
        self.assertEqual(self.json.serialize(obj), '{"a":{"func_name": "fff", "code":"        fff = lambda: 6\n"}}')
        fff = lambda x: 6
        obj = {"a": fff}
        self.assertEqual(self.json.serialize(obj), '{"a":{"func_name": "fff", "code":"        fff = lambda x: 6\n"}}')

    def testLex_string(self):
        self.assertEqual(self.json.lex_string('"test"'), ('test', ''))
        self.assertEqual(self.json.lex_string('"test":"testing strings"'), ('test', ':"testing strings"'))
        self.assertEqual(self.json.lex_string('"test":1, "test2": 3'), ('test', ':1, "test2": 3'))

    def testLex_number(self):
        self.assertEqual(self.json.lex_number('123: "test"'), (123, ': "test"'))
        self.assertEqual(self.json.lex_number('123: "test", 1234: "test2"'), (123, ': "test", 1234: "test2"'))

    def testLex_bool(self):
        self.assertEqual(self.json.lex_bool('true: 123'), (True, ': 123'))
        self.assertEqual(self.json.lex_bool('false: "false"'), (False, ': "false"'))

    def testLex_null(self):
        self.assertEqual(self.json.lex_null('null: "<- null key"'), (True, ': "<- null key"'))

    def testLex(self):
        self.assertEqual(self.json.lex('1: "a", "b": 2, null: "null", true: "True"'),
                         [1, ':', 'a', ',', 'b', ':', 2, ',', None, ':', 'null', ',', True, ':', 'True'])
        self.assertEqual(
            self.json.lex('{"now we can lex(translate to tokens)": "pretty much everything", "a": 1, 123: "abc"}'),
            ['{', 'now we can lex(translate to tokens)', ':', 'pretty much everything', ',', 'a', ':', 1, ',', 123, ':',
             'abc', '}'])

    def testParse_array(self):
        self.assertEqual(self.json.parse_array([1, ',', 2, ',', 3, ']'], is_buffer=False), ([1, 2, 3], []))

    def testParse_object(self):
        self.assertEqual(self.json.parse_object(['a', ':', '1', '}']), ({"a": '1'}, []))

    def testParse_json(self):
        self.assertEqual(self.json.parse_json(['{', 'a', ':', '[', 1, ',', 2, ',', 3, ']', ',', 1, ':', 2, '}'], is_buffer=False), ({1: 2, 'a': [1, 2, 3]}, []))

    def testParse(self):
        self.assertEqual(self.json.parse('{"a": [1, 2, 3], 1: 2}'), {1: 2, 'a': [1, 2, 3]})

    def testParse_lambda(self):
        # self.assertEqual(self.json.parse('{"a":{"func_name": "fff", "code":"fff = lambda:
        # 6\n"},"b":2}'), {"a":lambda:6, "b": 2})
        self.assertEqual(self.json.parse('{"a":{"func_name": "fff", "code":"fff = lambda: 6\n"},"b":2}')["a"](), 6)

    def testJSON_parser(self):
        obj = {'a': 1}
        str = '{"a":1}'
        self.assertEqual(self.json.serialize(obj), str)
        self.assertEqual(self.json.parse(str), obj)


if __name__ == "__main__":
    unittest.main()
