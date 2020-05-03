import typing

from . import exceptions, types


class CircularDependencyCircuitBreaker(types.Middleware):
    def __init__(self):
        self._requested_types: typing.Dict[types.DependencyType, int] = {}
        self._stack: typing.List[types.DependencyType] = []

    def execute(
        self,
        dependency_type: types.DependencyType,
        next_middleware: types.NextMiddleware,
    ):
        self._raise_if_circular_dependency(dependency_type)
        self._track(dependency_type)

        try:
            return next_middleware()
        finally:
            self._untrack(dependency_type)

    def _raise_if_circular_dependency(self, dependency_type: types.DependencyType):
        if dependency_type in self._requested_types:
            cycle = self._stack[self._requested_types[dependency_type] :] + [
                dependency_type
            ]
            raise exceptions.CircularDependency(cycle=cycle)

    def _track(self, dependency_type: types.DependencyType):
        self._requested_types[dependency_type] = len(self._stack)
        self._stack.append(dependency_type)

    def _untrack(self, dependency_type):
        del self._requested_types[dependency_type]
        self._stack.pop()


class Singleton(types.Middleware):
    def __init__(self):
        self._dependency_values: typing.Dict[types.DependencyType, typing.Any] = {}

    def execute(
        self,
        dependency_type: types.DependencyType,
        next_middleware: types.NextMiddleware,
    ):
        try:
            return self._dependency_values[dependency_type]
        except KeyError:
            pass

        dependency_value = next_middleware()
        self._dependency_values[dependency_type] = dependency_value
        return dependency_value
