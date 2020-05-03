import cargo

# 1. Define your components


class A:
    def __str__(self):
        return "A"


class B:
    def __init__(self, a: A):
        self.a = a


# 2. Create a cargo container

container = cargo.containers.Standard()


# 3. Register your components

container[A] = A
container[B] = B


# 4. Use cargo to initialize your components

b = container[B]


# 5. Use your components

print(b.a)
