import cargo


class A:
    pass


class B:
    pass


class Hello:
    def __init__(self, foo: A, bar: B):
        print(f"Hello {foo} and {bar}")


container = cargo.containers.Standard()

container[A] = A
container[B] = B
container[Hello] = Hello

# Prints: Hello <__main__.A object at 0x7f863b0fd450> and <__main__.B object at 0x7f863b09b810>
container[Hello]
