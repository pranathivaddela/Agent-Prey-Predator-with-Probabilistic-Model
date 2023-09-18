class A:
    def p(self):
        print('A')


class B:
    def p(self):
        print('B')


class C(B, A):
    pass

c = C()
c.p()