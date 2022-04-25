def test_func(testArg1, testArg2):
    print(111)
    return 1000


class B:
    def __init__(self):
        print('I\'m B!')

    def test(self):
        return 'testing some classes'


class A(B):
    def test2(self):
        print('YES! IT WORKS')
