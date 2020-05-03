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
