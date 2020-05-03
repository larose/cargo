import typing

import cargo


def test_function_factory():
    class A:
        pass

    class B:
        def __init__(self, a: A):
            self.a = a

    def b_factory(a: A):
        return B(a)

    container = cargo.containers.Standard()
    container[A] = A
    container[B] = b_factory

    b = container[B]

    assert b.a == container[A]


def test_class_factory():
    class A:
        pass

    class B:
        def __init__(self, a: A):
            self.a = a

    container = cargo.containers.Standard()
    container[A] = A
    container[B] = B

    b = container[B]

    assert b.a == container[A]


def test_full():
    class A:
        pass

    class B:
        def __init__(self, a: A):
            self.a = a

    class C:
        pass

    D = typing.NewType("D", str)

    class E:
        def __init__(self, b: B, c: C, d: D):
            self.b = b
            self.c = c
            self.d = d

    container = cargo.containers.Standard()

    def b_factory(a: A):
        return B(a)

    container[A] = lambda: A()
    container[B] = b_factory
    container[C] = C
    container[D] = "d"
    container[E] = E

    e = container[E]

    assert e.b == container[B]
    assert e.c == container[C]
    assert e.d == "d"
    assert e.b.a == container[A]


def test_same_factory_for_two_types():
    class A:
        pass

    class B(A):
        pass

    class C:
        def __init__(self, a: A, b: B):
            pass

    container = cargo.containers.Standard()
    container[A] = B
    container[B] = B
    container[C] = C

    assert isinstance(container[C], C)
