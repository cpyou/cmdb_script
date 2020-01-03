class A(object):
    def __init__(self):
        print('a.....')
        self.a = 'a'


class B(object):
    def __init__(self):
        print('b......')
        self.b = 'b'


class C(A, B):
    def __init__(self):
        super().__init__()
        self.c = 'c'


class C2(A, B):
    def __init__(self):
        super().__init__()
        B.__init__(self)
        self.c = 'c'


c = C()
print(c)
c2 = C2()
print(c2)
print('......')


