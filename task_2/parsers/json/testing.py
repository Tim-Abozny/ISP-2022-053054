from factory import Creator
import inspect


class Meta:
    def __init__(self, name, args):
        self.cl = type(name, (), args)


if __name__ == '__main__':
    pf = './MyFile.txt'
    pf = pf[2:]
    try:
        file = open(pf, 'r')
        my_str = file.read()
    except Exception as e:
        print('There is no such file by path: ' + pf)
    d = Creator.createDeserializer(my_str)
    cl = Meta('A', d)
    print(cl.cl.name)

    # o = {"a": lambda name: f'Hello {name}', "b": 2}
    # b = lambda i: i + 1
    # c = {"a": lambda i: {"i": i}}
    #
    # i = inspect.getsource(c["a"])
    # s = i[i.find("lambda"):]
    # left = 0
    # right = 0
    # for ind in range(len(s)):
    #     if s[ind] in ('{', '['):
    #         left += 1
    #     elif s[ind] in (')', '}', ','):
    #         right += 1
    # diff = right - left
    # for i in range(diff):
    #     if s.rfind(',') > s.rfind('}'):
    #         s = s[:s.rfind(',')]
    #     else:
    #         s = s[:s.rfind('}')]
    #
    # print(s)
