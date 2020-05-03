# Cargo

Cargo is a dependency injection library for Python.

Cargo is [simple to use](#getting-started), [typed](#cargo-is-typed),
[flexible](#cargo-is-flexible), [extensible](#cargo-is-extensible) and
[easy to debug](#cargo-is-easy-to-debug).


## Getting started

### Step 1: Install cargo

With pip:

```shell script
$ pip install cargo
```

With pipenv:

```shell script
$ pipenv install cargo
```

With poetry:

```shell script
$ poetry add cargo
```

### Step 2: Use cargo

[examples/intro.py](./examples/intro.py):

```python
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
```

## Features

All the examples are located in the [examples](examples) directory.


### Cargo is typed

Cargo uses the argument types to inject the dependencies; not their
names.

[examples/hello_dependencies.py](examples/hello_dependencies.py):

```python
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
```

### Cargo is flexible

Functions and methods can be used as factories; and objects as values.

[examples/factory_and_value.py](examples/factory_and_value.py):

```python
...

DatabaseURL = typing.NewType("DatabaseURL", str)

def database_client_factory(db_url: DatabaseURL) -> DatabaseClient:
    if db_url.startswith("mysql://"):
        return MysqlClient(db_url)

    if db_url.startswith("postgres://"):
        return PostgresClient(db_url)

    raise Exception(f"Invalid database url: {db_url}")


container = cargo.containers.Standard()

# Registers a factory
container[DatabaseClient] = database_client_factory

# Registers a value
container[DatabaseURL] = "mysql://user:password@host:3306/db"

db_client = container[DatabaseClient]

print(db_client)  # Prints: <__main__.MysqlClient object at 0x7f681975b390>
```



### Cargo is extensible

Cargo composes middlewares to create containers. The
[`Standard`](cargo/containers.py) container is just a stack of
opiniated middlewares. You can create your own types of containers
with the [middlewares](cargo/middlewares.py) you want, or even create
your own middlewares.


[examples/my_container.py](examples/my_container.py):

```python
import cargo


class LoggerMiddleware(cargo.types.Middleware):
    def execute(
        self,
        dependency_type: cargo.types.DependencyType,
        next_middleware: cargo.types.NextMiddleware,
    ):
        print(f"Start resolving {dependency_type}")
        dependency_value = next_middleware()
        print(f"End resolving {dependency_type}")
        return dependency_value


middleware_factories = [
    LoggerMiddleware,
    cargo.middlewares.CircularDependencyCircuitBreaker,
    cargo.middlewares.Singleton,
]
container = cargo.containers.create(middleware_factories)


class A:
    pass


class B:
    def __init__(self, a: A):
        pass


container[A] = A
container[B] = B

# Prints:
# Start resolving <class '__main__.B'>
# Start resolving <class '__main__.A'>
# End resolving <class '__main__.A'>
# End resolving <class '__main__.B'>
container[B]
```


### Cargo is easy to debug

#### Dependency not found

Cargo raises a [`DependencyNotFound`](cargo/exceptions.py) exception
with the missing dependency type when a dependency is not found.

[examples/dependency_not_found.py](examples/dependency_not_found.py):

```python
...

class A:
    def __init__(self, b: B):
        pass


class B:
    pass


container = cargo.containers.Standard()
container[A] = A
# Note: B has not been registered

# Raises cargo.exceptions.DependencyNotFound: <class '__main__.B'>
container[A]
```

#### Circular dependency

Cargo raises a [`CircularDependency`](cargo/exceptions.py) exception
with the dependency cycle when a circular dependency is detected.

[examples/circular_dependency.py](examples/circular_dependency.py):

```python
...

# Dependencies:
#   - A depends on B
#   - B depends on C
#   - C depends on D
#   - D depends on B
#
# Circular dependency cycle is: B -> C -> D -> B

...

container = cargo.containers.Standard()
container[A] = A
container[B] = B
container[C] = C
container[D] = D

# Raises cargo.exceptions.CircularDependency:
#   [<class '__main__.B'>, <class '__main__.C'>, <class '__main__.D'>, <class '__main__.B'>]
container[A]
```


## Contributors

- [Mathieu Larose](https://mathieularose.com)


## License

Cargo is licensed under the terms of the [MIT license](./LICENSE).


## Website

https://github.com/larose/cargo
